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
from thiscovery_lib.s3_utilities import Transfer


BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

FILES_TO_TRANSFER = [
    ("css", "sample.css"),
]


def get_git_revision():
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True,
        check=True,
        text=True,
    ).stdout.strip()


def main(s3_folder_name=None):
    if s3_folder_name is None:
        s3_folder_name = input("Please enter the target S3 folder name:").strip()
    revision = get_git_revision()
    transfer_client = Transfer()
    for folder, file in FILES_TO_TRANSFER:
        transfer_client.upload_public_file(
            file_path=os.path.join(BASE_DIR, folder, file),
            bucket_name="qualtrics-config-afs25",
            s3_path=f"{s3_folder_name}/{file}",
            **{"Metadata": {"revision": revision}},
        )


if __name__ == "__main__":
    main()
