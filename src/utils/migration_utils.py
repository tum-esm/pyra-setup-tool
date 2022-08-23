def run(from_dict: dict, from_version: str) -> tuple[dict, str]:
    if from_version == "4.0.4":
        # to_version = 4.0.5
        # TODO: modify rules
        return {}, "4.0.5"
    else:
        raise Exception(f'Unknown version "{from_version}"')
