# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from enum import Enum
from azure.core import CaseInsensitiveEnumMeta


class AuthenticationType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """An enumeration of possible authentication types when connecting."""

    NONE = "None"
    WINDOWS_AUTHENTICATION = "WindowsAuthentication"
    SQL_AUTHENTICATION = "SqlAuthentication"
    ACTIVE_DIRECTORY_INTEGRATED = "ActiveDirectoryIntegrated"
    ACTIVE_DIRECTORY_PASSWORD = "ActiveDirectoryPassword"


class AuthType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Authentication type used for accessing Azure Blob Storage."""

    ACCOUNT_KEY = "AccountKey"
    """Use an account key for authentication."""
    MANAGED_IDENTITY = "ManagedIdentity"
    """Use a managed identity for authentication."""


class BackupFileStatus(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """An enumeration of Status of the log backup file."""

    ARRIVED = "Arrived"
    QUEUED = "Queued"
    UPLOADING = "Uploading"
    UPLOADED = "Uploaded"
    RESTORING = "Restoring"
    RESTORED = "Restored"
    CANCELLED = "Cancelled"


class BackupMode(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """An enumeration of backup modes."""

    CREATE_BACKUP = "CreateBackup"
    EXISTING_BACKUP = "ExistingBackup"


class BackupType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Enum of the different backup types."""

    DATABASE = "Database"
    TRANSACTION_LOG = "TransactionLog"
    FILE = "File"
    DIFFERENTIAL_DATABASE = "DifferentialDatabase"
    DIFFERENTIAL_FILE = "DifferentialFile"
    PARTIAL = "Partial"
    DIFFERENTIAL_PARTIAL = "DifferentialPartial"


class CommandState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The state of the command. This is ignored if submitted."""

    UNKNOWN = "Unknown"
    ACCEPTED = "Accepted"
    RUNNING = "Running"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"


class CommandType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Command type."""

    MIGRATE_SYNC_COMPLETE_DATABASE = "Migrate.Sync.Complete.Database"
    MIGRATE_SQL_SERVER_AZURE_DB_SQL_MI_COMPLETE = "Migrate.SqlServer.AzureDbSqlMi.Complete"
    CANCEL = "cancel"
    FINISH = "finish"
    RESTART = "restart"


class CreatedByType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The type of identity that created the resource."""

    USER = "User"
    APPLICATION = "Application"
    MANAGED_IDENTITY = "ManagedIdentity"
    KEY = "Key"


class DatabaseCompatLevel(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """An enumeration of SQL Server database compatibility levels."""

    COMPAT_LEVEL80 = "CompatLevel80"
    COMPAT_LEVEL90 = "CompatLevel90"
    COMPAT_LEVEL100 = "CompatLevel100"
    COMPAT_LEVEL110 = "CompatLevel110"
    COMPAT_LEVEL120 = "CompatLevel120"
    COMPAT_LEVEL130 = "CompatLevel130"
    COMPAT_LEVEL140 = "CompatLevel140"


class DatabaseFileType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """An enumeration of SQL Server database file types."""

    ROWS = "Rows"
    LOG = "Log"
    FILESTREAM = "Filestream"
    NOT_SUPPORTED = "NotSupported"
    FULLTEXT = "Fulltext"


class DatabaseMigrationStage(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Current stage of migration."""

    NONE = "None"
    INITIALIZE = "Initialize"
    BACKUP = "Backup"
    FILE_COPY = "FileCopy"
    RESTORE = "Restore"
    COMPLETED = "Completed"


class DatabaseMigrationState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Database level migration state."""

    UNDEFINED = "UNDEFINED"
    INITIAL = "INITIAL"
    FULL_BACKUP_UPLOAD_START = "FULL_BACKUP_UPLOAD_START"
    LOG_SHIPPING_START = "LOG_SHIPPING_START"
    UPLOAD_LOG_FILES_START = "UPLOAD_LOG_FILES_START"
    CUTOVER_START = "CUTOVER_START"
    POST_CUTOVER_COMPLETE = "POST_CUTOVER_COMPLETE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"


class DatabaseState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """An enumeration of SQL Server Database states."""

    ONLINE = "Online"
    RESTORING = "Restoring"
    RECOVERING = "Recovering"
    RECOVERY_PENDING = "RecoveryPending"
    SUSPECT = "Suspect"
    EMERGENCY = "Emergency"
    OFFLINE = "Offline"
    COPYING = "Copying"
    OFFLINE_SECONDARY = "OfflineSecondary"


class DataMigrationResultCode(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Result code of the data migration."""

    INITIAL = "Initial"
    COMPLETED = "Completed"
    OBJECT_NOT_EXISTS_IN_SOURCE = "ObjectNotExistsInSource"
    OBJECT_NOT_EXISTS_IN_TARGET = "ObjectNotExistsInTarget"
    TARGET_OBJECT_IS_INACCESSIBLE = "TargetObjectIsInaccessible"
    FATAL_ERROR = "FatalError"


class ErrorType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Error type."""

    DEFAULT = "Default"
    WARNING = "Warning"
    ERROR = "Error"


class LoginMigrationStage(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Enum of the different stage of login migration."""

    NONE = "None"
    INITIALIZE = "Initialize"
    LOGIN_MIGRATION = "LoginMigration"
    ESTABLISH_USER_MAPPING = "EstablishUserMapping"
    ASSIGN_ROLE_MEMBERSHIP = "AssignRoleMembership"
    ASSIGN_ROLE_OWNERSHIP = "AssignRoleOwnership"
    ESTABLISH_SERVER_PERMISSIONS = "EstablishServerPermissions"
    ESTABLISH_OBJECT_PERMISSIONS = "EstablishObjectPermissions"
    COMPLETED = "Completed"


class LoginType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Enum mapping of SMO LoginType."""

    WINDOWS_USER = "WindowsUser"
    WINDOWS_GROUP = "WindowsGroup"
    SQL_LOGIN = "SqlLogin"
    CERTIFICATE = "Certificate"
    ASYMMETRIC_KEY = "AsymmetricKey"
    EXTERNAL_USER = "ExternalUser"
    EXTERNAL_GROUP = "ExternalGroup"


class ManagedServiceIdentityType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Type of managed service identity (where both SystemAssigned and UserAssigned types are
    allowed).
    """

    NONE = "None"
    SYSTEM_ASSIGNED = "SystemAssigned"
    USER_ASSIGNED = "UserAssigned"
    SYSTEM_ASSIGNED_USER_ASSIGNED = "SystemAssigned,UserAssigned"


class MigrationState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Current state of migration."""

    NONE = "None"
    IN_PROGRESS = "InProgress"
    FAILED = "Failed"
    WARNING = "Warning"
    COMPLETED = "Completed"
    SKIPPED = "Skipped"
    STOPPED = "Stopped"


class MigrationStatus(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Current status of migration."""

    DEFAULT = "Default"
    CONNECTING = "Connecting"
    SOURCE_AND_TARGET_SELECTED = "SourceAndTargetSelected"
    SELECT_LOGINS = "SelectLogins"
    CONFIGURED = "Configured"
    RUNNING = "Running"
    ERROR = "Error"
    STOPPED = "Stopped"
    COMPLETED = "Completed"
    COMPLETED_WITH_WARNINGS = "CompletedWithWarnings"


class MongoDbClusterType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The type of data source."""

    BLOB_CONTAINER = "BlobContainer"
    COSMOS_DB = "CosmosDb"
    MONGO_DB = "MongoDb"


class MongoDbErrorType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The type of error or warning."""

    ERROR = "Error"
    VALIDATION_ERROR = "ValidationError"
    WARNING = "Warning"


class MongoDbMigrationState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """MongoDbMigrationState."""

    NOT_STARTED = "NotStarted"
    VALIDATING_INPUT = "ValidatingInput"
    INITIALIZING = "Initializing"
    RESTARTING = "Restarting"
    COPYING = "Copying"
    INITIAL_REPLAY = "InitialReplay"
    REPLAYING = "Replaying"
    FINALIZING = "Finalizing"
    COMPLETE = "Complete"
    CANCELED = "Canceled"
    FAILED = "Failed"


class MongoDbProgressResultType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The type of progress object."""

    MIGRATION = "Migration"
    DATABASE = "Database"
    COLLECTION = "Collection"


class MongoDbReplication(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Describes how changes will be replicated from the source to the target. The default is OneTime."""

    DISABLED = "Disabled"
    ONE_TIME = "OneTime"
    CONTINUOUS = "Continuous"


class MongoDbShardKeyOrder(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The field ordering."""

    FORWARD = "Forward"
    REVERSE = "Reverse"
    HASHED = "Hashed"


class MongoMigrationStatus(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Migration Status."""

    NOT_STARTED = "NotStarted"
    IN_PROGRESS = "InProgress"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CANCELED = "Canceled"


class MySqlTargetPlatformType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """An enumeration of possible target types when migrating from MySQL."""

    SQL_SERVER = "SqlServer"
    AZURE_DB_FOR_MY_SQL = "AzureDbForMySQL"


class NameCheckFailureReason(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The reason why the name is not available, if nameAvailable is false."""

    ALREADY_EXISTS = "AlreadyExists"
    INVALID = "Invalid"


class ObjectType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """An enumeration of type of objects."""

    STORED_PROCEDURES = "StoredProcedures"
    TABLE = "Table"
    USER = "User"
    VIEW = "View"
    FUNCTION = "Function"


class OperationOrigin(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """OperationOrigin."""

    USER = "user"
    SYSTEM = "system"


class ProjectProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The project's provisioning state."""

    DELETING = "Deleting"
    SUCCEEDED = "Succeeded"


class ProjectSourcePlatform(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Source platform of the project."""

    SQL = "SQL"
    MY_SQL = "MySQL"
    POSTGRE_SQL = "PostgreSql"
    MONGO_DB = "MongoDb"
    UNKNOWN = "Unknown"


class ProjectTargetPlatform(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Target platform of the project."""

    SQLDB = "SQLDB"
    SQLMI = "SQLMI"
    AZURE_DB_FOR_MY_SQL = "AzureDbForMySql"
    AZURE_DB_FOR_POSTGRE_SQL = "AzureDbForPostgreSql"
    MONGO_DB = "MongoDb"
    UNKNOWN = "Unknown"


class ProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Provisioning State of migration. ProvisioningState as Succeeded implies that validations have
    been performed and migration has started.
    """

    PROVISIONING = "Provisioning"
    UPDATING = "Updating"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    CANCELED = "Canceled"


class ReplicateMigrationState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Wrapper for replicate reported migration states."""

    UNDEFINED = "UNDEFINED"
    VALIDATING = "VALIDATING"
    PENDING = "PENDING"
    COMPLETE = "COMPLETE"
    ACTION_REQUIRED = "ACTION_REQUIRED"
    FAILED = "FAILED"


class ResourceSkuCapacityScaleType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The scale type applicable to the SKU."""

    AUTOMATIC = "Automatic"
    MANUAL = "Manual"
    NONE = "None"


class ResourceSkuRestrictionsReasonCode(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The reason code for restriction."""

    QUOTA_ID = "QuotaId"
    NOT_AVAILABLE_FOR_SUBSCRIPTION = "NotAvailableForSubscription"


class ResourceSkuRestrictionsType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The type of restrictions."""

    LOCATION = "location"


class ResourceType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """ResourceType."""

    SQL_MI = "SqlMi"
    SQL_VM = "SqlVm"
    SQL_DB = "SqlDb"
    MONGO_TO_COSMOS_DB_MONGO = "MongoToCosmosDbMongo"


class ScenarioSource(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """An enumeration of source type."""

    ACCESS = "Access"
    DB2 = "DB2"
    MY_SQL = "MySQL"
    ORACLE = "Oracle"
    SQL = "SQL"
    SYBASE = "Sybase"
    POSTGRE_SQL = "PostgreSQL"
    MONGO_DB = "MongoDB"
    SQLRDS = "SQLRDS"
    MY_SQLRDS = "MySQLRDS"
    POSTGRE_SQLRDS = "PostgreSQLRDS"


class ScenarioTarget(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """An enumeration of target type."""

    SQL_SERVER = "SQLServer"
    SQLDB = "SQLDB"
    SQLDW = "SQLDW"
    SQLMI = "SQLMI"
    AZURE_DB_FOR_MY_SQL = "AzureDBForMySql"
    AZURE_DB_FOR_POSTGRES_SQL = "AzureDBForPostgresSQL"
    MONGO_DB = "MongoDB"


class SchemaMigrationOption(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Option for how schema is extracted and applied to target."""

    NONE = "None"
    EXTRACT_FROM_SOURCE = "ExtractFromSource"
    USE_STORAGE_FILE = "UseStorageFile"


class SchemaMigrationStage(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Current stage of schema migration."""

    NOT_STARTED = "NotStarted"
    VALIDATING_INPUTS = "ValidatingInputs"
    COLLECTING_OBJECTS = "CollectingObjects"
    DOWNLOADING_SCRIPT = "DownloadingScript"
    GENERATING_SCRIPT = "GeneratingScript"
    UPLOADING_SCRIPT = "UploadingScript"
    DEPLOYING_SCHEMA = "DeployingSchema"
    COMPLETED = "Completed"
    COMPLETED_WITH_WARNINGS = "CompletedWithWarnings"
    FAILED = "Failed"


class ServerLevelPermissionsGroup(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Permission group for validations. These groups will run a set of permissions for validating
    user activity. Select the permission group for the activity that you are performing.
    """

    DEFAULT = "Default"
    MIGRATION_FROM_SQL_SERVER_TO_AZURE_DB = "MigrationFromSqlServerToAzureDB"
    MIGRATION_FROM_SQL_SERVER_TO_AZURE_MI = "MigrationFromSqlServerToAzureMI"
    MIGRATION_FROM_MY_SQL_TO_AZURE_DB_FOR_MY_SQL = "MigrationFromMySQLToAzureDBForMySQL"
    MIGRATION_FROM_SQL_SERVER_TO_AZURE_VM = "MigrationFromSqlServerToAzureVM"


class ServiceProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The resource's provisioning state."""

    ACCEPTED = "Accepted"
    DELETING = "Deleting"
    DEPLOYING = "Deploying"
    STOPPED = "Stopped"
    STOPPING = "Stopping"
    STARTING = "Starting"
    FAILED_TO_START = "FailedToStart"
    FAILED_TO_STOP = "FailedToStop"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"


class ServiceScalability(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The scalability approach."""

    NONE = "none"
    MANUAL = "manual"
    AUTOMATIC = "automatic"


class Severity(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Severity of the validation error."""

    MESSAGE = "Message"
    WARNING = "Warning"
    ERROR = "Error"


class SqlSourcePlatform(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """An enumeration of source platform types."""

    SQL_ON_PREM = "SqlOnPrem"


class SsisMigrationOverwriteOption(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The overwrite option for SSIS object migration, only ignore and overwrite are supported in DMS
    (classic) now and future may add Reuse option for container object.
    """

    IGNORE = "Ignore"
    OVERWRITE = "Overwrite"


class SsisMigrationStage(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Current stage of SSIS migration."""

    NONE = "None"
    INITIALIZE = "Initialize"
    IN_PROGRESS = "InProgress"
    COMPLETED = "Completed"


class SsisStoreType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """An enumeration of supported source SSIS store type in DMS (classic)."""

    SSIS_CATALOG = "SsisCatalog"


class SyncDatabaseMigrationReportingState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Enum of the different state of database level online migration."""

    UNDEFINED = "UNDEFINED"
    CONFIGURING = "CONFIGURING"
    INITIALIAZING = "INITIALIAZING"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    READY_TO_COMPLETE = "READY_TO_COMPLETE"
    COMPLETING = "COMPLETING"
    COMPLETE = "COMPLETE"
    CANCELLING = "CANCELLING"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"
    VALIDATING = "VALIDATING"
    VALIDATION_COMPLETE = "VALIDATION_COMPLETE"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    RESTORE_IN_PROGRESS = "RESTORE_IN_PROGRESS"
    RESTORE_COMPLETED = "RESTORE_COMPLETED"
    BACKUP_IN_PROGRESS = "BACKUP_IN_PROGRESS"
    BACKUP_COMPLETED = "BACKUP_COMPLETED"


class SyncTableMigrationState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Enum of the different state of table level online migration."""

    BEFORE_LOAD = "BEFORE_LOAD"
    FULL_LOAD = "FULL_LOAD"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"
    ERROR = "ERROR"
    FAILED = "FAILED"


class TaskState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The state of the task. This is ignored if submitted."""

    UNKNOWN = "Unknown"
    QUEUED = "Queued"
    RUNNING = "Running"
    CANCELED = "Canceled"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    FAILED_INPUT_VALIDATION = "FailedInputValidation"
    FAULTED = "Faulted"


class TaskType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Task type."""

    CONNECT_MONGO_DB = "Connect.MongoDb"
    CONNECT_TO_SOURCE_SQL_SERVER = "ConnectToSource.SqlServer"
    CONNECT_TO_SOURCE_SQL_SERVER_SYNC = "ConnectToSource.SqlServer.Sync"
    CONNECT_TO_SOURCE_POSTGRE_SQL_SYNC = "ConnectToSource.PostgreSql.Sync"
    CONNECT_TO_SOURCE_MY_SQL = "ConnectToSource.MySql"
    CONNECT_TO_SOURCE_ORACLE_SYNC = "ConnectToSource.Oracle.Sync"
    CONNECT_TO_TARGET_SQL_DB = "ConnectToTarget.SqlDb"
    CONNECT_TO_TARGET_SQL_DB_SYNC = "ConnectToTarget.SqlDb.Sync"
    CONNECT_TO_TARGET_AZURE_DB_FOR_POSTGRE_SQL_SYNC = "ConnectToTarget.AzureDbForPostgreSql.Sync"
    CONNECT_TO_TARGET_ORACLE_AZURE_DB_FOR_POSTGRE_SQL_SYNC = "ConnectToTarget.Oracle.AzureDbForPostgreSql.Sync"
    CONNECT_TO_TARGET_AZURE_SQL_DB_MI = "ConnectToTarget.AzureSqlDbMI"
    CONNECT_TO_TARGET_AZURE_SQL_DB_MI_SYNC_LRS = "ConnectToTarget.AzureSqlDbMI.Sync.LRS"
    CONNECT_TO_TARGET_AZURE_DB_FOR_MY_SQL = "ConnectToTarget.AzureDbForMySql"
    GET_USER_TABLES_SQL = "GetUserTables.Sql"
    GET_USER_TABLES_AZURE_SQL_DB_SYNC = "GetUserTables.AzureSqlDb.Sync"
    GET_USER_TABLES_ORACLE = "GetUserTablesOracle"
    GET_USER_TABLES_POSTGRE_SQL = "GetUserTablesPostgreSql"
    GET_USER_TABLES_MY_SQL = "GetUserTablesMySql"
    MIGRATE_MONGO_DB = "Migrate.MongoDb"
    MIGRATE_SQL_SERVER_AZURE_SQL_DB_MI = "Migrate.SqlServer.AzureSqlDbMI"
    MIGRATE_SQL_SERVER_AZURE_SQL_DB_MI_SYNC_LRS = "Migrate.SqlServer.AzureSqlDbMI.Sync.LRS"
    MIGRATE_SQL_SERVER_SQL_DB = "Migrate.SqlServer.SqlDb"
    MIGRATE_SQL_SERVER_AZURE_SQL_DB_SYNC = "Migrate.SqlServer.AzureSqlDb.Sync"
    MIGRATE_MY_SQL_AZURE_DB_FOR_MY_SQL_SYNC = "Migrate.MySql.AzureDbForMySql.Sync"
    MIGRATE_MY_SQL_AZURE_DB_FOR_MY_SQL = "Migrate.MySql.AzureDbForMySql"
    MIGRATE_POSTGRE_SQL_AZURE_DB_FOR_POSTGRE_SQL_SYNC_V2 = "Migrate.PostgreSql.AzureDbForPostgreSql.SyncV2"
    MIGRATE_ORACLE_AZURE_DB_FOR_POSTGRE_SQL_SYNC = "Migrate.Oracle.AzureDbForPostgreSql.Sync"
    VALIDATE_MIGRATION_INPUT_SQL_SERVER_SQL_DB_SYNC = "ValidateMigrationInput.SqlServer.SqlDb.Sync"
    VALIDATE_MIGRATION_INPUT_SQL_SERVER_AZURE_SQL_DB_MI = "ValidateMigrationInput.SqlServer.AzureSqlDbMI"
    VALIDATE_MIGRATION_INPUT_SQL_SERVER_AZURE_SQL_DB_MI_SYNC_LRS = (
        "ValidateMigrationInput.SqlServer.AzureSqlDbMI.Sync.LRS"
    )
    VALIDATE_MONGO_DB = "Validate.MongoDb"
    VALIDATE_ORACLE_AZURE_DB_POSTGRE_SQL_SYNC = "Validate.Oracle.AzureDbPostgreSql.Sync"
    GET_TDE_CERTIFICATES_SQL = "GetTDECertificates.Sql"
    MIGRATE_SSIS = "Migrate.Ssis"
    SERVICE_CHECK_OCI = "Service.Check.OCI"
    SERVICE_UPLOAD_OCI = "Service.Upload.OCI"
    SERVICE_INSTALL_OCI = "Service.Install.OCI"
    MIGRATE_SCHEMA_SQL_SERVER_SQL_DB = "MigrateSchemaSqlServerSqlDb"


class UpdateActionType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Type of the actual difference for the compared object, while performing schema comparison."""

    DELETED_ON_TARGET = "DeletedOnTarget"
    CHANGED_ON_TARGET = "ChangedOnTarget"
    ADDED_ON_TARGET = "AddedOnTarget"


class ValidationStatus(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Current status of the validation."""

    DEFAULT = "Default"
    NOT_STARTED = "NotStarted"
    INITIALIZED = "Initialized"
    IN_PROGRESS = "InProgress"
    COMPLETED = "Completed"
    COMPLETED_WITH_ISSUES = "CompletedWithIssues"
    STOPPED = "Stopped"
    FAILED = "Failed"
