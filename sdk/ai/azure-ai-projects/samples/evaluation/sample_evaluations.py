# pylint: disable=line-too-long,useless-suppression
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

"""
DESCRIPTION:
    Given an AIProjectClient, this sample demonstrates how to use the synchronous
    `.evaluations` methods to create, get and list evaluations.

USAGE:
    python sample_evaluations.py

    Before running the sample:

    pip install azure-ai-projects azure-identity

    Set these environment variables with your own values:
    1) PROJECT_ENDPOINT - Required. The Azure AI Project endpoint, as found in the overview page of your
       Azure AI Foundry project.
    2) CONNECTION_NAME - Required. The name of the Azure Storage Account connection to use for uploading files.
    3) DATASET_NAME - Optional. The name of the Dataset to create and use in this sample.
    4) DATASET_VERSION - Optional. The version of the Dataset to create and use in this sample.
    6) DATA_FOLDER - Optional. The folder path where the data files for upload are located.
"""

import os
from mimetypes import inited

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    Evaluation,
    InputDataset,
    EvaluatorConfiguration,
    EvaluatorIds,
    DatasetVersion,
)

endpoint = os.environ[
    "PROJECT_ENDPOINT"
]  # Sample : https://<account_name>.services.ai.azure.com/api/projects/<project_name>
model_endpoint = os.environ["MODEL_ENDPOINT"]  # Sample : https://<account_name>.services.ai.azure.com
model_api_key = os.environ["MODEL_API_KEY"]
model_deployment_name = os.environ["MODEL_DEPLOYMENT_NAME"]  # Sample : gpt-4o-mini
dataset_name = os.environ.get("DATASET_NAME", "dataset-test")
dataset_version = os.environ.get("DATASET_VERSION", "1.0")

# Construct the paths to the data folder and data file used in this sample
script_dir = os.path.dirname(os.path.abspath(__file__))
data_folder = os.environ.get("DATA_FOLDER", os.path.join(script_dir, "data_folder"))
data_file = os.path.join(data_folder, "sample_data_evaluation.jsonl")

with DefaultAzureCredential(exclude_interactive_browser_credential=False) as credential:

    with AIProjectClient(endpoint=endpoint, credential=credential) as project_client:

        # [START evaluations_sample]
        print("Upload a single file and create a new Dataset to reference the file.")
        dataset: DatasetVersion = project_client.datasets.upload_file(
            name=dataset_name,
            version=dataset_version,
            file_path=data_file,
        )
        print(dataset)

        print("Create an evaluation")
        evaluation: Evaluation = Evaluation(
            display_name="Sample Evaluation Test",
            description="Sample evaluation for testing",
            # Sample Dataset Id : azureai://accounts/<account_name>/projects/<project_name>/data/<dataset_name>/versions/<version>
            data=InputDataset(id=dataset.id if dataset.id else ""),
            evaluators={
                "relevance": EvaluatorConfiguration(
                    id=EvaluatorIds.RELEVANCE.value,
                    init_params={
                        "deployment_name": model_deployment_name,
                    },
                    data_mapping={
                        "query": "${data.query}",
                        "response": "${data.response}",
                    },
                ),
                "violence": EvaluatorConfiguration(
                    id=EvaluatorIds.VIOLENCE.value,
                    init_params={
                        "azure_ai_project": endpoint,
                    },
                ),
                "bleu_score": EvaluatorConfiguration(
                    id=EvaluatorIds.BLEU_SCORE.value,
                ),
            },
        )

        evaluation_response: Evaluation = project_client.evaluations.create(
            evaluation,
            headers={
                "model-endpoint": model_endpoint,
                "model-api-key": model_api_key,
            },
        )
        print(evaluation_response)

        print("Get evaluation")
        get_evaluation_response: Evaluation = project_client.evaluations.get(evaluation_response.name)

        print(get_evaluation_response)

        print("List evaluations")
        for evaluation in project_client.evaluations.list():
            print(evaluation)

        # [END evaluations_sample]
