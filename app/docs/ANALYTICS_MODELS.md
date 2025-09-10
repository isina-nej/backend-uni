# مدل‌های تحلیلی و هوش مصنوعی - Analytics and AI Models

## مدل‌های SQLAlchemy برای سیستم تحلیلی

```python
# app/models/analytics.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class AnalysisType(str, enum.Enum):
    DESCRIPTIVE = "توصیفی"
    DIAGNOSTIC = "تشخیصی"
    PREDICTIVE = "پیش‌بینی"
    PRESCRIPTIVE = "تجویزی"
    COGNITIVE = "شناختی"

class ModelType(str, enum.Enum):
    LINEAR_REGRESSION = "رگرسیون خطی"
    LOGISTIC_REGRESSION = "رگرسیون لجستیک"
    DECISION_TREE = "درخت تصمیم"
    RANDOM_FOREST = "جنگل تصادفی"
    GRADIENT_BOOSTING = "تقویت گرادیان"
    NEURAL_NETWORK = "شبکه عصبی"
    SVM = "ماشین بردار پشتیبان"
    K_MEANS = "K-Means"
    TIME_SERIES = "سری زمانی"
    NLP_MODEL = "مدل پردازش زبان"
    RECOMMENDATION = "سیستم پیشنهاد"
    ANOMALY_DETECTION = "تشخیص ناهنجاری"

class ModelStatus(str, enum.Enum):
    DRAFT = "پیش‌نویس"
    TRAINING = "در حال آموزش"
    TRAINED = "آموزش دیده"
    VALIDATING = "در حال اعتبارسنجی"
    VALIDATED = "اعتبارسنجی شده"
    DEPLOYED = "استقرار یافته"
    RETRAINING = "در حال آموزش مجدد"
    FAILED = "ناموفق"
    DEPRECATED = "منسوخ شده"

class MetricType(str, enum.Enum):
    ACCURACY = "دقت"
    PRECISION = "دقت مثبت"
    RECALL = "بازخوانی"
    F1_SCORE = "امتیاز F1"
    AUC_ROC = "AUC-ROC"
    MSE = "خطای مربعات میانی"
    RMSE = "ریشه خطای مربعات میانی"
    MAE = "خطای مطلق میانی"
    R_SQUARED = "R مربع"
    CONFUSION_MATRIX = "ماتریس درهم‌ریختگی"

class PredictionType(str, enum.Enum):
    BINARY = "دودویی"
    MULTICLASS = "چندکلاسه"
    REGRESSION = "رگرسیون"
    TIME_SERIES = "سری زمانی"
    RECOMMENDATION = "پیشنهاد"
    CLUSTERING = "خوشه‌بندی"
    ANOMALY = "ناهنجاری"

class DataSourceType(str, enum.Enum):
    DATABASE_TABLE = "جدول پایگاه داده"
    API_ENDPOINT = "نقطه پایانی API"
    FILE_UPLOAD = "بارگذاری فایل"
    STREAMING_DATA = "داده جاری"
    EXTERNAL_SYSTEM = "سیستم خارجی"

class VisualizationType(str, enum.Enum):
    BAR_CHART = "نمودار میله‌ای"
    LINE_CHART = "نمودار خطی"
    PIE_CHART = "نمودار دایره‌ای"
    SCATTER_PLOT = "نمودار پراکندگی"
    HEATMAP = "نقشه حرارتی"
    HISTOGRAM = "هیستوگرام"
    BOX_PLOT = "نمودار جعبه‌ای"
    TREEMAP = "درخت نقشه"
    DASHBOARD = "داشبورد"

class AIModel(Base):
    __tablename__ = 'ai_models'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    model_type = Column(Enum(ModelType), nullable=False)
    analysis_type = Column(Enum(AnalysisType), nullable=False)
    prediction_type = Column(Enum(PredictionType), nullable=False)
    framework = Column(String(50), nullable=False)  # scikit-learn, tensorflow, pytorch, etc.
    version = Column(String(20), default="1.0")
    status = Column(Enum(ModelStatus), default=ModelStatus.DRAFT)
    configuration = Column(JSON)
    hyperparameters = Column(JSON)
    feature_columns = Column(JSON)
    target_column = Column(String(100))
    training_data_source = Column(JSON)
    validation_data_source = Column(JSON)
    test_data_source = Column(JSON)
    model_file_path = Column(String(500))
    model_metrics = Column(JSON)
    accuracy_score = Column(Float)
    training_start_time = Column(DateTime)
    training_end_time = Column(DateTime)
    training_duration_seconds = Column(Integer)
    last_prediction_time = Column(DateTime)
    prediction_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    auto_retrain = Column(Boolean, default=False)
    retrain_schedule = Column(JSON)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approval_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by_employee = relationship("Employee", foreign_keys=[created_by])
    approved_by_employee = relationship("Employee", foreign_keys=[approved_by])

class ModelTraining(Base):
    __tablename__ = 'model_trainings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(Integer, ForeignKey('ai_models.id'), nullable=False)
    training_id = Column(String(20), unique=True, nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    duration_seconds = Column(Integer)
    status = Column(String(20), default='running')  # running, completed, failed
    training_data_size = Column(Integer)
    validation_data_size = Column(Integer)
    hyperparameters_used = Column(JSON)
    metrics = Column(JSON)
    loss_history = Column(JSON)
    validation_metrics = Column(JSON)
    model_file_path = Column(String(500))
    log_file_path = Column(String(500))
    error_message = Column(Text)
    initiated_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    model = relationship("AIModel", back_populates="trainings")
    initiated_by_employee = relationship("Employee", foreign_keys=[initiated_by])

class ModelPrediction(Base):
    __tablename__ = 'model_predictions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(Integer, ForeignKey('ai_models.id'), nullable=False)
    prediction_id = Column(String(20), unique=True, nullable=False)
    input_data = Column(JSON)
    prediction_result = Column(JSON)
    confidence_score = Column(Float)
    prediction_time = Column(DateTime, default=datetime.utcnow)
    processing_time_ms = Column(Integer)
    status = Column(String(20), default='success')  # success, failed, timeout
    error_message = Column(Text)
    requested_by = Column(Integer, ForeignKey('employees.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    model = relationship("AIModel", back_populates="predictions")
    requested_by_employee = relationship("Employee", foreign_keys=[requested_by])

class AnalyticsReport(Base):
    __tablename__ = 'analytics_reports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    report_type = Column(String(50), nullable=False)  # academic, financial, operational, etc.
    analysis_type = Column(Enum(AnalysisType), nullable=False)
    data_source = Column(JSON)
    filters = Column(JSON)
    aggregations = Column(JSON)
    calculations = Column(JSON)
    visualizations = Column(JSON)
    schedule = Column(JSON)
    is_scheduled = Column(Boolean, default=False)
    last_run_date = Column(DateTime)
    next_run_date = Column(DateTime)
    status = Column(String(20), default='active')  # active, inactive, error
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by_employee = relationship("Employee", foreign_keys=[created_by])

class ReportExecution(Base):
    __tablename__ = 'report_executions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    report_id = Column(Integer, ForeignKey('analytics_reports.id'), nullable=False)
    execution_id = Column(String(20), unique=True, nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    duration_seconds = Column(Integer)
    status = Column(String(20), default='running')  # running, completed, failed
    records_processed = Column(Integer)
    results = Column(JSON)
    visualizations_data = Column(JSON)
    file_path = Column(String(500))
    error_message = Column(Text)
    executed_by = Column(Integer, ForeignKey('employees.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    report = relationship("AnalyticsReport", back_populates="executions")
    executed_by_employee = relationship("Employee", foreign_keys=[executed_by])

class DataVisualization(Base):
    __tablename__ = 'data_visualizations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    visualization_type = Column(Enum(VisualizationType), nullable=False)
    data_source = Column(JSON)
    configuration = Column(JSON)
    filters = Column(JSON)
    refresh_interval_minutes = Column(Integer, default=60)
    is_public = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by_employee = relationship("Employee", foreign_keys=[created_by])

class KPI(Base):
    __tablename__ = 'kpis'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    category = Column(String(50), nullable=False)  # academic, financial, operational, etc.
    formula = Column(Text, nullable=False)
    data_source = Column(JSON)
    target_value = Column(Float)
    threshold_good = Column(Float)
    threshold_warning = Column(Float)
    threshold_critical = Column(Float)
    unit = Column(String(20))
    calculation_frequency = Column(String(20), default='daily')  # hourly, daily, weekly, monthly
    last_calculated_value = Column(Float)
    last_calculation_date = Column(DateTime)
    trend = Column(String(20))  # increasing, decreasing, stable
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by_employee = relationship("Employee", foreign_keys=[created_by])

class KPICalculation(Base):
    __tablename__ = 'kpi_calculations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    kpi_id = Column(Integer, ForeignKey('kpis.id'), nullable=False)
    calculation_date = Column(DateTime, nullable=False)
    value = Column(Float, nullable=False)
    target_value = Column(Float)
    variance = Column(Float)
    variance_percentage = Column(Float)
    status = Column(String(20))  # good, warning, critical
    calculation_parameters = Column(JSON)
    notes = Column(Text)
    calculated_by = Column(String(20), default='system')  # system, manual
    manual_calculated_by = Column(Integer, ForeignKey('employees.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    kpi = relationship("KPI", back_populates="calculations")
    manual_calculated_by_employee = relationship("Employee", foreign_keys=[manual_calculated_by])

class PredictiveModel(Base):
    __tablename__ = 'predictive_models'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    model_type = Column(Enum(ModelType), nullable=False)
    prediction_target = Column(String(100), nullable=False)
    prediction_horizon = Column(String(50))  # days, weeks, months, semesters
    accuracy_threshold = Column(Float, default=0.8)
    confidence_interval = Column(Float, default=0.95)
    data_window_days = Column(Integer, default=365)
    features = Column(JSON)
    model_parameters = Column(JSON)
    performance_metrics = Column(JSON)
    last_trained_date = Column(DateTime)
    next_training_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by_employee = relationship("Employee", foreign_keys=[created_by])

class Prediction(Base):
    __tablename__ = 'predictions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(Integer, ForeignKey('predictive_models.id'), nullable=False)
    prediction_id = Column(String(20), unique=True, nullable=False)
    input_data = Column(JSON)
    prediction_result = Column(JSON)
    confidence_score = Column(Float)
    prediction_date = Column(DateTime, nullable=False)
    target_date = Column(DateTime)
    actual_value = Column(Float)
    prediction_error = Column(Float)
    accuracy_score = Column(Float)
    status = Column(String(20), default='predicted')  # predicted, verified, failed
    notes = Column(Text)
    created_by = Column(Integer, ForeignKey('employees.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    model = relationship("PredictiveModel", back_populates="predictions")
    created_by_employee = relationship("Employee", foreign_keys=[created_by])

class RecommendationEngine(Base):
    __tablename__ = 'recommendation_engines'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    algorithm = Column(String(50), nullable=False)  # collaborative, content-based, hybrid
    target_entity = Column(String(50), nullable=False)  # courses, professors, study_groups, etc.
    data_source = Column(JSON)
    similarity_metrics = Column(JSON)
    recommendation_rules = Column(JSON)
    min_similarity_threshold = Column(Float, default=0.3)
    max_recommendations = Column(Integer, default=10)
    cache_expiry_hours = Column(Integer, default=24)
    performance_metrics = Column(JSON)
    last_updated_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by_employee = relationship("Employee", foreign_keys=[created_by])

class Recommendation(Base):
    __tablename__ = 'recommendations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    engine_id = Column(Integer, ForeignKey('recommendation_engines.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    target_entity_type = Column(String(50), nullable=False)
    target_entity_id = Column(Integer, nullable=False)
    recommendation_score = Column(Float, nullable=False)
    recommendation_reason = Column(Text)
    context_data = Column(JSON)
    is_viewed = Column(Boolean, default=False)
    viewed_date = Column(DateTime)
    is_accepted = Column(Boolean, default=False)
    accepted_date = Column(DateTime)
    feedback_score = Column(Integer)  # 1-5 scale
    feedback_comment = Column(Text)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    engine = relationship("RecommendationEngine", back_populates="recommendations")
    user = relationship("Employee", foreign_keys=[user_id])

class AnomalyDetection(Base):
    __tablename__ = 'anomaly_detections'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    detection_type = Column(String(50), nullable=False)  # statistical, machine_learning, rule_based
    data_source = Column(JSON)
    algorithm = Column(String(50))
    parameters = Column(JSON)
    sensitivity = Column(Float, default=0.95)  # 0-1 scale
    detection_window_hours = Column(Integer, default=24)
    baseline_period_days = Column(Integer, default=30)
    alert_threshold = Column(Float, default=0.8)
    is_active = Column(Boolean, default=True)
    last_detection_date = Column(DateTime)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by_employee = relationship("Employee", foreign_keys=[created_by])

class DetectedAnomaly(Base):
    __tablename__ = 'detected_anomalies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    detection_id = Column(Integer, ForeignKey('anomaly_detections.id'), nullable=False)
    anomaly_id = Column(String(20), unique=True, nullable=False)
    detection_date = Column(DateTime, default=datetime.utcnow)
    severity = Column(String(20), nullable=False)  # low, medium, high, critical
    confidence_score = Column(Float, nullable=False)
    anomaly_data = Column(JSON)
    expected_value = Column(Float)
    actual_value = Column(Float)
    deviation_percentage = Column(Float)
    description = Column(Text)
    investigation_status = Column(String(20), default='pending')  # pending, investigating, resolved, false_positive
    investigated_by = Column(Integer, ForeignKey('employees.id'))
    investigation_date = Column(DateTime)
    investigation_notes = Column(Text)
    resolution = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    detection = relationship("AnomalyDetection", back_populates="anomalies")
    investigated_by_employee = relationship("Employee", foreign_keys=[investigated_by])

class DataQualityRule(Base):
    __tablename__ = 'data_quality_rules'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    rule_type = Column(String(50), nullable=False)  # completeness, accuracy, consistency, timeliness
    table_name = Column(String(100), nullable=False)
    column_name = Column(String(100))
    rule_definition = Column(JSON)
    severity = Column(String(20), default='medium')  # low, medium, high, critical
    threshold_value = Column(Float)
    is_active = Column(Boolean, default=True)
    last_check_date = Column(DateTime)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by_employee = relationship("Employee", foreign_keys=[created_by])

class DataQualityCheck(Base):
    __tablename__ = 'data_quality_checks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_id = Column(Integer, ForeignKey('data_quality_rules.id'), nullable=False)
    check_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), nullable=False)  # pass, fail, warning
    records_checked = Column(Integer)
    records_failed = Column(Integer)
    failure_percentage = Column(Float)
    error_details = Column(JSON)
    execution_time_seconds = Column(Float)
    checked_by = Column(String(20), default='system')  # system, manual
    manual_checked_by = Column(Integer, ForeignKey('employees.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    rule = relationship("DataQualityRule", back_populates="checks")
    manual_checked_by_employee = relationship("Employee", foreign_keys=[manual_checked_by])

class AnalyticsDashboard(Base):
    __tablename__ = 'analytics_dashboards'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    dashboard_type = Column(String(50), nullable=False)  # executive, operational, academic, financial
    layout_config = Column(JSON)
    widgets = Column(JSON)
    filters = Column(JSON)
    refresh_interval_minutes = Column(Integer, default=30)
    is_public = Column(Boolean, default=False)
    access_permissions = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by_employee = relationship("Employee", foreign_keys=[created_by])
```

## Pydantic Schemas برای سیستم تحلیلی

```python
# app/schemas/analytics.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class AnalysisType(str, Enum):
    DESCRIPTIVE = "توصیفی"
    DIAGNOSTIC = "تشخیصی"
    PREDICTIVE = "پیش‌بینی"
    PRESCRIPTIVE = "تجویزی"
    COGNITIVE = "شناختی"

class ModelType(str, Enum):
    LINEAR_REGRESSION = "رگرسیون خطی"
    LOGISTIC_REGRESSION = "رگرسیون لجستیک"
    DECISION_TREE = "درخت تصمیم"
    RANDOM_FOREST = "جنگل تصادفی"
    GRADIENT_BOOSTING = "تقویت گرادیان"
    NEURAL_NETWORK = "شبکه عصبی"
    SVM = "ماشین بردار پشتیبان"
    K_MEANS = "K-Means"
    TIME_SERIES = "سری زمانی"
    NLP_MODEL = "مدل پردازش زبان"
    RECOMMENDATION = "سیستم پیشنهاد"
    ANOMALY_DETECTION = "تشخیص ناهنجاری"

class ModelStatus(str, Enum):
    DRAFT = "پیش‌نویس"
    TRAINING = "در حال آموزش"
    TRAINED = "آموزش دیده"
    VALIDATING = "در حال اعتبارسنجی"
    VALIDATED = "اعتبارسنجی شده"
    DEPLOYED = "استقرار یافته"
    RETRAINING = "در حال آموزش مجدد"
    FAILED = "ناموفق"
    DEPRECATED = "منسوخ شده"

class MetricType(str, Enum):
    ACCURACY = "دقت"
    PRECISION = "دقت مثبت"
    RECALL = "بازخوانی"
    F1_SCORE = "امتیاز F1"
    AUC_ROC = "AUC-ROC"
    MSE = "خطای مربعات میانی"
    RMSE = "ریشه خطای مربعات میانی"
    MAE = "خطای مطلق میانی"
    R_SQUARED = "R مربع"
    CONFUSION_MATRIX = "ماتریس درهم‌ریختگی"

class PredictionType(str, Enum):
    BINARY = "دودویی"
    MULTICLASS = "چندکلاسه"
    REGRESSION = "رگرسیون"
    TIME_SERIES = "سری زمانی"
    RECOMMENDATION = "پیشنهاد"
    CLUSTERING = "خوشه‌بندی"
    ANOMALY = "ناهنجاری"

class DataSourceType(str, Enum):
    DATABASE_TABLE = "جدول پایگاه داده"
    API_ENDPOINT = "نقطه پایانی API"
    FILE_UPLOAD = "بارگذاری فایل"
    STREAMING_DATA = "داده جاری"
    EXTERNAL_SYSTEM = "سیستم خارجی"

class VisualizationType(str, Enum):
    BAR_CHART = "نمودار میله‌ای"
    LINE_CHART = "نمودار خطی"
    PIE_CHART = "نمودار دایره‌ای"
    SCATTER_PLOT = "نمودار پراکندگی"
    HEATMAP = "نقشه حرارتی"
    HISTOGRAM = "هیستوگرام"
    BOX_PLOT = "نمودار جعبه‌ای"
    TREEMAP = "درخت نقشه"
    DASHBOARD = "داشبورد"

# AI Model schemas
class AIModelBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    description: Optional[str] = None
    model_type: ModelType
    analysis_type: AnalysisType
    prediction_type: PredictionType
    framework: str = Field(..., min_length=1, max_length=50)
    version: str = "1.0"
    configuration: Optional[Dict[str, Any]] = None
    hyperparameters: Optional[Dict[str, Any]] = None
    feature_columns: Optional[Dict[str, Any]] = None
    target_column: Optional[str] = None
    training_data_source: Optional[Dict[str, Any]] = None
    validation_data_source: Optional[Dict[str, Any]] = None
    test_data_source: Optional[Dict[str, Any]] = None
    auto_retrain: bool = False
    retrain_schedule: Optional[Dict[str, Any]] = None

class AIModelCreate(AIModelBase):
    pass

class AIModelUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    description: Optional[str] = None
    model_type: Optional[ModelType] = None
    analysis_type: Optional[AnalysisType] = None
    prediction_type: Optional[PredictionType] = None
    framework: Optional[str] = Field(None, min_length=1, max_length=50)
    version: Optional[str] = None
    status: Optional[ModelStatus] = None
    configuration: Optional[Dict[str, Any]] = None
    hyperparameters: Optional[Dict[str, Any]] = None
    feature_columns: Optional[Dict[str, Any]] = None
    target_column: Optional[str] = None
    training_data_source: Optional[Dict[str, Any]] = None
    validation_data_source: Optional[Dict[str, Any]] = None
    test_data_source: Optional[Dict[str, Any]] = None
    model_file_path: Optional[str] = None
    model_metrics: Optional[Dict[str, Any]] = None
    accuracy_score: Optional[float] = None
    training_start_time: Optional[datetime] = None
    training_end_time: Optional[datetime] = None
    training_duration_seconds: Optional[int] = None
    last_prediction_time: Optional[datetime] = None
    auto_retrain: Optional[bool] = None
    retrain_schedule: Optional[Dict[str, Any]] = None
    approved_by: Optional[int] = None
    approval_date: Optional[datetime] = None
    is_active: Optional[bool] = None

class AIModel(AIModelBase):
    id: int
    status: ModelStatus
    model_file_path: Optional[str] = None
    model_metrics: Optional[Dict[str, Any]] = None
    accuracy_score: Optional[float] = None
    training_start_time: Optional[datetime] = None
    training_end_time: Optional[datetime] = None
    training_duration_seconds: Optional[int] = None
    last_prediction_time: Optional[datetime] = None
    prediction_count: int
    is_active: bool
    created_by: int
    approved_by: Optional[int] = None
    approval_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AIModelWithDetails(AIModel):
    created_by_employee: Optional[Dict[str, Any]] = None
    approved_by_employee: Optional[Dict[str, Any]] = None
    trainings_count: int = 0
    predictions_count: int = 0

# Model Training schemas
class ModelTrainingBase(BaseModel):
    training_data_size: Optional[int] = None
    validation_data_size: Optional[int] = None
    hyperparameters_used: Optional[Dict[str, Any]] = None

class ModelTrainingCreate(ModelTrainingBase):
    model_id: int

class ModelTraining(ModelTrainingBase):
    id: int
    model_id: int
    training_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    status: str
    metrics: Optional[Dict[str, Any]] = None
    loss_history: Optional[Dict[str, Any]] = None
    validation_metrics: Optional[Dict[str, Any]] = None
    model_file_path: Optional[str] = None
    log_file_path: Optional[str] = None
    error_message: Optional[str] = None
    initiated_by: int
    created_at: datetime

    class Config:
        from_attributes = True

class ModelTrainingWithDetails(ModelTraining):
    model: Optional[Dict[str, Any]] = None
    initiated_by_employee: Optional[Dict[str, Any]] = None

# Model Prediction schemas
class ModelPredictionBase(BaseModel):
    input_data: Optional[Dict[str, Any]] = None

class ModelPredictionCreate(ModelPredictionBase):
    model_id: int

class ModelPrediction(ModelPredictionBase):
    id: int
    model_id: int
    prediction_id: str
    prediction_result: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = None
    prediction_time: datetime
    processing_time_ms: Optional[int] = None
    status: str
    error_message: Optional[str] = None
    requested_by: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ModelPredictionWithDetails(ModelPrediction):
    model: Optional[Dict[str, Any]] = None
    requested_by_employee: Optional[Dict[str, Any]] = None

# Analytics Report schemas
class AnalyticsReportBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    description: Optional[str] = None
    report_type: str = Field(..., min_length=1, max_length=50)
    analysis_type: AnalysisType
    data_source: Optional[Dict[str, Any]] = None
    filters: Optional[Dict[str, Any]] = None
    aggregations: Optional[Dict[str, Any]] = None
    calculations: Optional[Dict[str, Any]] = None
    visualizations: Optional[Dict[str, Any]] = None
    schedule: Optional[Dict[str, Any]] = None
    is_scheduled: bool = False

class AnalyticsReportCreate(AnalyticsReportBase):
    pass

class AnalyticsReportUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    description: Optional[str] = None
    report_type: Optional[str] = Field(None, min_length=1, max_length=50)
    analysis_type: Optional[AnalysisType] = None
    data_source: Optional[Dict[str, Any]] = None
    filters: Optional[Dict[str, Any]] = None
    aggregations: Optional[Dict[str, Any]] = None
    calculations: Optional[Dict[str, Any]] = None
    visualizations: Optional[Dict[str, Any]] = None
    schedule: Optional[Dict[str, Any]] = None
    is_scheduled: Optional[bool] = None
    last_run_date: Optional[datetime] = None
    next_run_date: Optional[datetime] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None

class AnalyticsReport(AnalyticsReportBase):
    id: int
    last_run_date: Optional[datetime] = None
    next_run_date: Optional[datetime] = None
    status: str
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AnalyticsReportWithDetails(AnalyticsReport):
    created_by_employee: Optional[Dict[str, Any]] = None
    executions_count: int = 0

# KPI schemas
class KPIBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    description: Optional[str] = None
    category: str = Field(..., min_length=1, max_length=50)
    formula: str = Field(..., min_length=1)
    data_source: Optional[Dict[str, Any]] = None
    target_value: Optional[float] = None
    threshold_good: Optional[float] = None
    threshold_warning: Optional[float] = None
    threshold_critical: Optional[float] = None
    unit: Optional[str] = None
    calculation_frequency: str = "daily"

class KPICreate(KPIBase):
    pass

class KPIUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    description: Optional[str] = None
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    formula: Optional[str] = Field(None, min_length=1)
    data_source: Optional[Dict[str, Any]] = None
    target_value: Optional[float] = None
    threshold_good: Optional[float] = None
    threshold_warning: Optional[float] = None
    threshold_critical: Optional[float] = None
    unit: Optional[str] = None
    calculation_frequency: Optional[str] = None
    last_calculated_value: Optional[float] = None
    last_calculation_date: Optional[datetime] = None
    trend: Optional[str] = None
    is_active: Optional[bool] = None

class KPI(KPIBase):
    id: int
    last_calculated_value: Optional[float] = None
    last_calculation_date: Optional[datetime] = None
    trend: Optional[str] = None
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class KPIWithDetails(KPI):
    created_by_employee: Optional[Dict[str, Any]] = None
    calculations_count: int = 0
    current_value: Optional[float] = None
    current_status: Optional[str] = None

# Predictive Model schemas
class PredictiveModelBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    description: Optional[str] = None
    model_type: ModelType
    prediction_target: str = Field(..., min_length=1, max_length=100)
    prediction_horizon: Optional[str] = None
    accuracy_threshold: float = 0.8
    confidence_interval: float = 0.95
    data_window_days: int = 365
    features: Optional[Dict[str, Any]] = None
    model_parameters: Optional[Dict[str, Any]] = None

class PredictiveModelCreate(PredictiveModelBase):
    pass

class PredictiveModelUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    description: Optional[str] = None
    model_type: Optional[ModelType] = None
    prediction_target: Optional[str] = Field(None, min_length=1, max_length=100)
    prediction_horizon: Optional[str] = None
    accuracy_threshold: Optional[float] = None
    confidence_interval: Optional[float] = None
    data_window_days: Optional[int] = None
    features: Optional[Dict[str, Any]] = None
    model_parameters: Optional[Dict[str, Any]] = None
    performance_metrics: Optional[Dict[str, Any]] = None
    last_trained_date: Optional[datetime] = None
    next_training_date: Optional[datetime] = None
    is_active: Optional[bool] = None

class PredictiveModel(PredictiveModelBase):
    id: int
    performance_metrics: Optional[Dict[str, Any]] = None
    last_trained_date: Optional[datetime] = None
    next_training_date: Optional[datetime] = None
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PredictiveModelWithDetails(PredictiveModel):
    created_by_employee: Optional[Dict[str, Any]] = None
    predictions_count: int = 0
    accuracy_score: Optional[float] = None

# Recommendation Engine schemas
class RecommendationEngineBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    description: Optional[str] = None
    algorithm: str = Field(..., min_length=1, max_length=50)
    target_entity: str = Field(..., min_length=1, max_length=50)
    data_source: Optional[Dict[str, Any]] = None
    similarity_metrics: Optional[Dict[str, Any]] = None
    recommendation_rules: Optional[Dict[str, Any]] = None
    min_similarity_threshold: float = 0.3
    max_recommendations: int = 10
    cache_expiry_hours: int = 24

class RecommendationEngineCreate(RecommendationEngineBase):
    pass

class RecommendationEngineUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    description: Optional[str] = None
    algorithm: Optional[str] = Field(None, min_length=1, max_length=50)
    target_entity: Optional[str] = Field(None, min_length=1, max_length=50)
    data_source: Optional[Dict[str, Any]] = None
    similarity_metrics: Optional[Dict[str, Any]] = None
    recommendation_rules: Optional[Dict[str, Any]] = None
    min_similarity_threshold: Optional[float] = None
    max_recommendations: Optional[int] = None
    cache_expiry_hours: Optional[int] = None
    performance_metrics: Optional[Dict[str, Any]] = None
    last_updated_date: Optional[datetime] = None
    is_active: Optional[bool] = None

class RecommendationEngine(RecommendationEngineBase):
    id: int
    performance_metrics: Optional[Dict[str, Any]] = None
    last_updated_date: Optional[datetime] = None
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RecommendationEngineWithDetails(RecommendationEngine):
    created_by_employee: Optional[Dict[str, Any]] = None
    recommendations_count: int = 0

# Anomaly Detection schemas
class AnomalyDetectionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    description: Optional[str] = None
    detection_type: str = Field(..., min_length=1, max_length=50)
    data_source: Optional[Dict[str, Any]] = None
    algorithm: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    sensitivity: float = 0.95
    detection_window_hours: int = 24
    baseline_period_days: int = 30
    alert_threshold: float = 0.8

class AnomalyDetectionCreate(AnomalyDetectionBase):
    pass

class AnomalyDetectionUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    description: Optional[str] = None
    detection_type: Optional[str] = Field(None, min_length=1, max_length=50)
    data_source: Optional[Dict[str, Any]] = None
    algorithm: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    sensitivity: Optional[float] = None
    detection_window_hours: Optional[int] = None
    baseline_period_days: Optional[int] = None
    alert_threshold: Optional[float] = None
    last_detection_date: Optional[datetime] = None
    is_active: Optional[bool] = None

class AnomalyDetection(AnomalyDetectionBase):
    id: int
    last_detection_date: Optional[datetime] = None
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AnomalyDetectionWithDetails(AnomalyDetection):
    created_by_employee: Optional[Dict[str, Any]] = None
    anomalies_count: int = 0

# Pagination schemas
class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_prev: bool

# Search and filter schemas
class AIModelSearchFilters(BaseModel):
    model_type: Optional[ModelType] = None
    analysis_type: Optional[AnalysisType] = None
    prediction_type: Optional[PredictionType] = None
    framework: Optional[str] = None
    status: Optional[ModelStatus] = None
    is_active: Optional[bool] = None
    created_by: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    search: Optional[str] = None

class AnalyticsReportSearchFilters(BaseModel):
    report_type: Optional[str] = None
    analysis_type: Optional[AnalysisType] = None
    is_scheduled: Optional[bool] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None
    created_by: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    search: Optional[str] = None

class KPISearchFilters(BaseModel):
    category: Optional[str] = None
    calculation_frequency: Optional[str] = None
    is_active: Optional[bool] = None
    created_by: Optional[int] = None
    search: Optional[str] = None

class PredictiveModelSearchFilters(BaseModel):
    model_type: Optional[ModelType] = None
    prediction_target: Optional[str] = None
    is_active: Optional[bool] = None
    created_by: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    search: Optional[str] = None

class RecommendationEngineSearchFilters(BaseModel):
    algorithm: Optional[str] = None
    target_entity: Optional[str] = None
    is_active: Optional[bool] = None
    created_by: Optional[int] = None
    search: Optional[str] = None

class AnomalyDetectionSearchFilters(BaseModel):
    detection_type: Optional[str] = None
    is_active: Optional[bool] = None
    created_by: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    search: Optional[str] = None
```

این پیاده‌سازی کامل مدل‌های تحلیلی و هوش مصنوعی شامل تمام ویژگی‌های مورد نیاز برای تحلیل داده‌های پیشرفته، یادگیری ماشین، و تصمیم‌گیری هوشمند دانشگاهی ایران است.
