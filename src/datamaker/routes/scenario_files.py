"""Client for scenario file operations - CRUD functionality for file persistence in scenarios."""

import os
import base64
import mimetypes
import requests
from typing import Dict, List, Optional, Union, BinaryIO
from .base import BaseClient
from ..error import DataMakerError


class ScenarioFilesClient(BaseClient):
    """Client for scenario file operations.

    Provides CRUD functionality for persisting and managing files within scenarios.
    Files stored through this client will appear in the 'Recently Added Files' folder
    on the DataMaker scenarios page.
    """

    def get_scenario_files(
        self, scenario_id: Optional[str] = None, folder: Optional[str] = None
    ) -> List[Dict]:
        """Fetch all files for a scenario.

        Args:
            scenario_id: Optional scenario ID. Falls back to DATAMAKER_SCENARIO_ID env var.
            folder: Optional folder filter ("uploads" or "outputs").

        Returns:
            Dictionary containing files list, storage usage, and storage limit.

        Raises:
            DataMakerError: If scenario_id is not provided and not available in environment.
        """
        # Get scenario_id from environment if not provided
        scenario_id = scenario_id or os.environ.get("DATAMAKER_SCENARIO_ID")

        if not scenario_id:
            raise DataMakerError(
                "scenario_id is required. Either pass it as a parameter or set "
                "DATAMAKER_SCENARIO_ID environment variable."
            )

        endpoint = f"/scenarios/{scenario_id}/files"
        if folder:
            endpoint += f"?folder={folder}"
        response = self._make_request("GET", endpoint)
        return response.json()

    def get_scenario_file(
        self, file_id: str, scenario_id: Optional[str] = None
    ) -> Dict:
        """Get metadata for a specific file by ID.

        Args:
            file_id: The unique identifier of the file.
            scenario_id: Optional scenario ID. Falls back to DATAMAKER_SCENARIO_ID env var.

        Returns:
            File metadata dictionary with refreshed presigned URL.

        Raises:
            DataMakerError: If scenario_id is not provided and not available in environment.
        """
        # Get scenario_id from environment if not provided
        scenario_id = scenario_id or os.environ.get("DATAMAKER_SCENARIO_ID")

        if not scenario_id:
            raise DataMakerError(
                "scenario_id is required. Either pass it as a parameter or set "
                "DATAMAKER_SCENARIO_ID environment variable."
            )

        response = self._make_request(
            "GET", f"/scenarios/{scenario_id}/files/{file_id}"
        )
        return response.json()

    def download_scenario_file(
        self, file_id: str, scenario_id: Optional[str] = None
    ) -> bytes:
        """Download a file's content by ID.

        Args:
            file_id: The unique identifier of the file.
            scenario_id: Optional scenario ID. Falls back to DATAMAKER_SCENARIO_ID env var.

        Returns:
            The file content as bytes.

        Raises:
            DataMakerError: If scenario_id is not provided and not available in environment.
        """
        # Get file metadata with presigned URL first
        file_metadata = self.get_scenario_file(file_id, scenario_id)

        if not file_metadata.get("presignedUrl"):
            raise DataMakerError(f"No presigned URL available for file: {file_id}")

        # Download file using presigned URL
        presigned_url = file_metadata["presignedUrl"]
        download_response = requests.get(presigned_url, timeout=30)

        if download_response.status_code == 404:
            raise DataMakerError(f"File not found: {file_id}")
        elif download_response.status_code != 200:
            raise DataMakerError(
                f"Failed to download file: HTTP {download_response.status_code}"
            )

        return download_response.content

    def download_scenario_file_to_path(
        self, file_id: str, destination_path: str, scenario_id: Optional[str] = None
    ) -> str:
        """Download a file and save it to a local path.

        Args:
            file_id: The unique identifier of the file.
            destination_path: Local file path to save the downloaded content.
            scenario_id: Optional scenario ID. Falls back to DATAMAKER_SCENARIO_ID env var.

        Returns:
            The destination path where the file was saved.

        Raises:
            DataMakerError: If scenario_id is not provided and not available in environment.
        """
        content = self.download_scenario_file(file_id, scenario_id)
        with open(destination_path, "wb") as f:
            f.write(content)
        return destination_path

    def create_scenario_file(
        self,
        name: str,
        content: Union[str, bytes, BinaryIO],
        scenario_id: Optional[str] = None,
        team_id: Optional[str] = None,
        project_id: Optional[str] = None,
        description: Optional[str] = None,
        mime_type: Optional[str] = None,
        folder_id: Optional[str] = None,
    ) -> Dict:
        """Create/upload a new file in a scenario.

        Args:
            name: The filename (e.g., 'data.json', 'config.yaml').
            content: The file content - can be a string, bytes, or file-like object.
            scenario_id: Optional scenario ID. Falls back to DATAMAKER_SCENARIO_ID env var.
            team_id: Optional team ID. Falls back to DATAMAKER_TEAM_ID env var.
            project_id: Optional project ID to associate with. Falls back to DATAMAKER_PROJECT_ID env var.
            description: Optional description of the file.
            mime_type: Optional MIME type. If not provided, will be guessed from filename.
            folder_id: Optional folder ID to place the file in.

        Returns:
            The created file metadata dictionary.

        Raises:
            DataMakerError: If required IDs are not provided and not available in environment.
        """
        # Get required IDs from environment if not provided
        scenario_id = scenario_id or os.environ.get("DATAMAKER_SCENARIO_ID")
        team_id = team_id or os.environ.get("DATAMAKER_TEAM_ID")
        project_id = project_id or os.environ.get("DATAMAKER_PROJECT_ID")

        if not scenario_id:
            raise DataMakerError(
                "scenario_id is required. Either pass it as a parameter or set "
                "DATAMAKER_SCENARIO_ID environment variable."
            )

        if not team_id:
            raise DataMakerError(
                "team_id is required. Either pass it as a parameter or set "
                "DATAMAKER_TEAM_ID environment variable."
            )
        # Handle different content types
        if isinstance(content, str):
            content_bytes = content.encode("utf-8")
        elif hasattr(content, "read"):
            content_bytes = content.read()
        else:
            content_bytes = content

        # Encode content as base64 for API transmission
        content_base64 = base64.b64encode(content_bytes).decode("utf-8")

        # Guess MIME type if not provided
        if not mime_type:
            mime_type, _ = mimetypes.guess_type(name)
            if not mime_type:
                mime_type = "application/octet-stream"

        file_data = {
            "name": name,
            "content": content_base64,
            "scenarioId": scenario_id,
            "teamId": team_id,
            "mimeType": mime_type,
            "size": len(content_bytes),
        }

        if project_id:
            file_data["projectId"] = project_id
        if description:
            file_data["description"] = description
        if folder_id:
            file_data["folderId"] = folder_id

        response = self._make_request("POST", "/scenario-files", json=file_data)
        return response.json()

    def upload_scenario_file_from_path(
        self,
        file_path: str,
        scenario_id: Optional[str] = None,
        team_id: Optional[str] = None,
        project_id: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        folder_id: Optional[str] = None,
        folder: str = "uploads",
    ) -> Dict:
        """Upload a file from a local path to a scenario using multipart upload.

        Args:
            file_path: Path to the local file to upload.
            scenario_id: Optional scenario ID. Falls back to DATAMAKER_SCENARIO_ID env var.
            team_id: Optional team ID. Falls back to DATAMAKER_TEAM_ID env var (not used for upload).
            project_id: Optional project ID to associate with. Falls back to DATAMAKER_PROJECT_ID env var (not used for upload).
            name: Optional filename. If not provided, uses the original filename.
            description: Optional description of the file (not used for multipart upload).
            folder_id: Optional folder ID to place the file in (not used for multipart upload).
            folder: Folder to upload to ("uploads" or "outputs", default: "uploads").

        Returns:
            The created file metadata dictionary.

        Raises:
            DataMakerError: If file not found or required IDs are not provided and not available in environment.
        """
        # Get required IDs from environment if not provided
        scenario_id = scenario_id or os.environ.get("DATAMAKER_SCENARIO_ID")

        if not scenario_id:
            raise DataMakerError(
                "scenario_id is required. Either pass it as a parameter or set "
                "DATAMAKER_SCENARIO_ID environment variable."
            )

        if not os.path.exists(file_path):
            raise DataMakerError(f"File not found: {file_path}")

        filename = name or os.path.basename(file_path)

        # Use multipart upload endpoint for better performance
        with open(file_path, "rb") as f:
            files = {"file": (filename, f)}
            data = {"folder": folder}

            response = self._make_request(
                "POST",
                f"/scenarios/{scenario_id}/files/upload",
                files=files,
                data=data,
            )

        result = response.json()
        return result.get("file", result)

    def delete_scenario_file(
        self, file_id: str, scenario_id: Optional[str] = None
    ) -> Dict:
        """Delete a file by ID.

        Args:
            file_id: The unique identifier of the file to delete.
            scenario_id: Optional scenario ID. Falls back to DATAMAKER_SCENARIO_ID env var.

        Returns:
            Confirmation response.

        Raises:
            DataMakerError: If scenario_id is not provided and not available in environment.
        """
        # Get scenario_id from environment if not provided
        scenario_id = scenario_id or os.environ.get("DATAMAKER_SCENARIO_ID")

        if not scenario_id:
            raise DataMakerError(
                "scenario_id is required. Either pass it as a parameter or set "
                "DATAMAKER_SCENARIO_ID environment variable."
            )

        response = self._make_request(
            "DELETE", f"/scenarios/{scenario_id}/files/{file_id}"
        )
        return response.json()

    def read_file_by_path(
        self,
        file_path: str,
        storage_base_url: Optional[str] = None,
    ) -> bytes:
        """Read a file directly from storage by its path.

        This method allows you to read files from the storage bucket using the
        file path copied from the workspace files modal. It's useful for accessing
        files uploaded to scenarios from within Python scripts.

        The method first queries the API to get a presigned URL for the file,
        then downloads the file content using that URL.

        Args:
            file_path: The file path (key) in storage. This is typically copied from
                      the workspace files modal using the "Copy path" button.
                      Example: "scenarios/team-id/project-id/scenario-id/workspace/uploads/filename.txt"
            storage_base_url: Deprecated. This parameter is ignored as the method now uses
                             the API to get presigned URLs instead of direct storage access.

        Returns:
            The file content as bytes.

        Raises:
            DataMakerError: If the file cannot be read or doesn't exist.

        Example:
            >>> client = DataMaker(api_key="your-key")
            >>> # Copy path from UI: "scenarios/.../workspace/uploads/data.json"
            >>> content = client.read_file_by_path("scenarios/.../workspace/uploads/data.json")
            >>> data = json.loads(content.decode('utf-8'))
        """
        try:
            # Get file metadata with presigned URL from API
            response = self._make_request(
                "GET", f"/workspace-files/by-key?key={file_path}"
            )
            file_data = response.json()

            if not file_data.get("presignedUrl"):
                raise DataMakerError(
                    f"No presigned URL available for file: {file_path}"
                )

            # Download file using presigned URL
            presigned_url = file_data["presignedUrl"]
            download_response = requests.get(presigned_url, timeout=30)

            if download_response.status_code == 404:
                raise DataMakerError(f"File not found at path: {file_path}")
            elif download_response.status_code != 200:
                raise DataMakerError(
                    f"Failed to download file: HTTP {download_response.status_code}"
                )

            return download_response.content

        except DataMakerError:
            raise
        except requests.RequestException as e:
            raise DataMakerError(f"Failed to read file from storage: {str(e)}")
        except Exception as e:
            raise DataMakerError(f"Failed to read file: {str(e)}")

    def read_file_by_path_as_text(
        self,
        file_path: str,
        storage_base_url: Optional[str] = None,
        encoding: str = "utf-8",
    ) -> str:
        """Read a file directly from storage by its path and return as text.

        Convenience method that reads a file and decodes it as text.

        Args:
            file_path: The file path (key) in storage.
            storage_base_url: Optional base URL for the storage bucket.
            encoding: Text encoding to use (default: 'utf-8').

        Returns:
            The file content as a string.

        Example:
            >>> client = DataMaker(api_key="your-key")
            >>> content = client.read_file_by_path_as_text("scenarios/abc123/uploads/data.txt")
            >>> print(content)
        """
        content = self.read_file_by_path(file_path, storage_base_url)
        return content.decode(encoding)

    def save_file(
        self,
        file_path: str,
        scenario_id: Optional[str] = None,
        team_id: Optional[str] = None,
        project_id: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        folder_id: Optional[str] = None,
        folder: str = "uploads",
    ) -> Dict:
        """Convenience method to save a local file to workspace storage.

        This method simplifies uploading files by automatically pulling required
        context (scenario_id) from environment variables if not provided.
        This is especially useful in DataMaker sandbox environments where these
        variables are pre-configured.

        Args:
            file_path: Path to the local file to save to workspace.
            scenario_id: Optional scenario ID. Falls back to DATAMAKER_SCENARIO_ID env var.
            team_id: Optional team ID (deprecated, not used for multipart upload).
            project_id: Optional project ID (deprecated, not used for multipart upload).
            name: Optional filename. If not provided, uses the original filename.
            description: Optional description of the file (deprecated, not used for multipart upload).
            folder_id: Optional folder ID (deprecated, not used for multipart upload).
            folder: Folder to upload to ("uploads" or "outputs", default: "uploads").

        Returns:
            The created file metadata dictionary.

        Raises:
            DataMakerError: If scenario_id is not provided and not available in environment.

        Example:
            >>> # In a DataMaker sandbox environment:
            >>> dm = DataMaker()
            >>> result = dm.save_file("test_file.txt")
            >>> print(f"File saved: {result['name']}")

            >>> # Or specify IDs explicitly:
            >>> result = dm.save_file(
            ...     "test_file.txt",
            ...     scenario_id="scenario-123"
            ... )
        """
        # Get required IDs from environment if not provided
        scenario_id = scenario_id or os.environ.get("DATAMAKER_SCENARIO_ID")

        if not scenario_id:
            raise DataMakerError(
                "scenario_id is required. Either pass it as a parameter or set "
                "DATAMAKER_SCENARIO_ID environment variable."
            )

        return self.upload_scenario_file_from_path(
            file_path=file_path,
            scenario_id=scenario_id,
            name=name,
            folder=folder,
        )
