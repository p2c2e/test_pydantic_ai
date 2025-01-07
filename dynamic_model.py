from pydantic import create_model, BaseModel
from typing import Any, Dict

def create_pydantic_model_from_schema(schema: Dict[str, Any]) -> BaseModel:
    """
    Dynamically creates a Pydantic model from a JSON Schema.

    Args:
        schema (dict): The JSON Schema to use for the model definition.

    Returns:
        BaseModel: A dynamically created Pydantic model.
    """
    fields = {}
    required = schema.get("required", [])

    # Parse properties in the schema
    for field_name, field_info in schema.get("properties", {}).items():
        field_type = field_info.get("type", "string")  # Default to string if type is not specified

        # Map JSON Schema types to Python types
        python_type = {
            "string": str,
            "integer": int,
            "number": float,
            "boolean": bool,
            "array": list,
            "object": dict,
        }.get(field_type, Any)

        # Define the field with its default or a placeholder
        default = ... if field_name in required else None
        fields[field_name] = (python_type, default)

    # Dynamically create the model
    return create_model(schema.get("title", "DynamicModel"), **fields)

if __name__ == "__main__":

    # Example usage
    json_schema = {
        "title": "ExampleModel",
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "is_active": {"type": "boolean"},
        },
        "required": ["name", "age"],
    }

    DynamicModel = create_pydantic_model_from_schema(json_schema)

    # Use the dynamically created model
    instance = DynamicModel(name="Alice", age=30, is_active=True)
    print(instance.model_dump())