from src.main import DataMaker
from src.template import Template

# Create an instance of DataMaker
datamaker = DataMaker()


def main():
    # Generate data using the template
    result = datamaker.generate_from_template_id(
        template_id="cm2114bwg0001evbhfqo2seul", quantity=2
    )
    print(result)


if __name__ == "__main__":
    main()
