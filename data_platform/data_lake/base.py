from enum import Enum
from constructs import Construct
from aws_cdk import Duration
from aws_cdk import (aws_s3 as s3, )



from data_platform.environment import Environment

class DataLakeLayer(Enum):
    RAW = 'raw'
    PROCESSED = 'processed'
    AGGREGATED = 'aggregated'



class BaseDataLakeBucket(s3.Bucket):
    def __init__(self, scope: Construct, deploy_env:Environment, layer: DataLakeLayer, **kwargs):

        self.layer = layer
        self.deploy_env = deploy_env
        self.obj_name = f"s3-dataplatform-{self.deploy_env.value}-data-lake-{self.layer.value}"

        super().__init__(
                scope,
                id=self.obj_name,
                bucket_name=self.obj_name,
                block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                encryption=s3.BucketEncryption.S3_MANAGED,
                versioned=True,
                **kwargs

                )


        @property
        def default_block_public_access(self):
            return s3.BlockPublicAccess(
                    ignore_public_acls=True,
                    block_public_acls=True,
                    block_public_policy=True,
                    restric_public_buckets=True

                    )


        @property
        def default_encryption(self):
            return s3.BucketEncryption.S3_MANAGED

        def set_default_lifecycle_rules(self):

            self.add_lifecycle_rule(
                    abort_incomplete_multipart_upload_after=Duration.days(7),
                    enabled=True

                    )

            self.add_lifecycle_rule(
                    noncurrent_version_transitions=[
                        s3.NoncurrentVersionTransition(
                            storage_class=s3.StorageClass.INFREQUENT_ACCESS,
                            transition_after=Duration.days(30)
                            ),
                        s3.NoncurrentVersionTransition(
                            storage_class=s3.StorageClass.GLACIER,
                        transition_after=Dutarion.days(60)
                        )
                    ]
                )

            self.add_lifecycle_rule(
                    noncurrent_version_expiration=Duration.days(360)
                    )



