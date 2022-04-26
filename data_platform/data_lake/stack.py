from data_platform.data_lake.base import BaseDataLakeBucket, DataLakeLayer
from aws_cdk import Stack, Construct, Duration
from aws_cdk import (aws_s3 as s3, )
from data_platform import active_environment


class DataLakeStack(Stack):
    def __init__(self, scope: Construct, **kwargs) -> None:
        self.deploy_env = active_environment
        super().__init__(scope, id='f{self.deploy_env.value}-data-lake-stack', **kwargs)

        self.data_lake_raw_bucket = BaseDataLakeBucket(
            self,
            deploy_env=self.deploy_env,
            layer=DataLakeLayer.RAW

            )

        self.data_lake_raw_bucket.add_lifecycle_rule(
            transitions=[
                s3.Transition(
                    storage_class=s3.StorageClass.INTELLIGENT_TIERING,
                    transition_after=Duration.days(90),
                ),
                s3.Transition(
                    storage_class=s3.StorageClass.GLACIER,
                    transition_after=Duration.days(360)
                    )

                ],
            enabled=True

            )


        # Data Lake Processed

        self.data_lake_processed_bucket = BaseDataLakeBucket(
            self,
            deploy_env=self.deploy_env,
            layer=DataLakeLayer.PROCESSED

            )


        # Data Lake Aggregated
        self.data_lake_curated_bucket = BaseDataLakeBucket(
            self,
            deploy_env=self.deploy_env,
            layer=DataLakeLayer.AGGREGATED

            )


