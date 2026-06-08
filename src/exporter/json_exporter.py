import json


class JSONExporter:

    def export(self, data, output_path):

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data.model_dump(),
                f,
                ensure_ascii=False,
                indent=4
            )