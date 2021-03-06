#
#   Thiscovery API - THIS Institute’s citizen science platform
#   Copyright (C) 2019 THIS Institute
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   A copy of the GNU Affero General Public License is available in the
#   docs folder of this project.  It is also available www.gnu.org/licenses/
#
import local.dev_config  # sets env variables TEST_ON_AWS and AWS_TEST_API
import local.secrets  # sets env variables THISCOVERY_AFS25_PROFILE and THISCOVERY_AMP205_PROFILE
import os
import subprocess
import thiscovery_lib.utilities as utils
from thiscovery_lib.s3_utilities import Transfer
from thiscovery_lib.ssm_utilities import SsmClient


BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

FILES_TO_TRANSFER = [
    (os.path.join("public", "build", "css"), "bundle.css"),
    (os.path.join("public", "build", "css"), "bundle.min.css"),
    (os.path.join("public", "build", "css", "images"), "ui-icons_444444_256x240.png"),
    (os.path.join("public", "build", "css", "images"), "ui-icons_555555_256x240.png"),
    (os.path.join("public", "build", "css", "images"), "ui-icons_777620_256x240.png"),
    (os.path.join("public", "build", "css", "images"), "ui-icons_777777_256x240.png"),
    (os.path.join("public", "build", "css", "images"), "ui-icons_cc0000_256x240.png"),
    (os.path.join("public", "build", "css", "images"), "ui-icons_ffffff_256x240.png"),
    (os.path.join("public", "build", "js"), "bundle.js"),
    (os.path.join("public", "build", "js"), "bundle.min.js"),
]

ext_to_content_type_map = {
    "css": "text/css",
    "js": "application/x-javascript",
}


class S3transferManager:
    def __init__(self):
        ssm_client = SsmClient()
        self.bucket_name = ssm_client.get_parameter("qualtrics")["static-files-bucket"]
        self.logger = utils.get_logger()

    @staticmethod
    def get_git_revision():
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            check=True,
            text=True,
        ).stdout.strip()

    def main(self, s3_folder_name=None):
        if s3_folder_name is None:
            s3_folder_name = input("Please enter the target S3 folder name:").strip()
        revision = self.get_git_revision()
        transfer_client = Transfer()
        self.logger.debug("Bucket", extra={"bucket_name": self.bucket_name})
        for folder, file in FILES_TO_TRANSFER:
            ext = os.path.splitext(file)[1].lstrip(".")
            kwargs = {"Metadata": {"revision": revision}}
            content_type = ext_to_content_type_map.get(ext)
            if content_type:
                kwargs.update({"ContentType": content_type})
            transfer_client.upload_public_file(
                file_path=os.path.join(BASE_DIR, folder, file),
                bucket_name=self.bucket_name,
                s3_path=f"{s3_folder_name}/{folder}/{file}",
                **kwargs,
            )


if __name__ == "__main__":
    s3_transfer_manager = S3transferManager()
    s3_transfer_manager.main()
