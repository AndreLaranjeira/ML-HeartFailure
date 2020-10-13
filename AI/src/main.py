# Program to train an AI to predict heart failure.

# Classes and methods imports.
from keras import Input
from keras.layers.core import Dense

# User module imports.
from argument_parser import ArgumentParserModule
from data_extractors import DatasetExtractor, SeedExtractor
from model_evaluator import ModelEvaluator
from training_models import KerasSequential, RandomForest

# Program metadata.
PROGRAM_NAME = 'heart_failure_prediction'
VERSION_NUM = '1.0.0'

# Argument parser.
argparser = ArgumentParserModule(PROGRAM_NAME, VERSION_NUM)
argparser.add_default_args()
args = argparser.parse_args()

# Extract the data.
dataset_extractor = DatasetExtractor(
    dataset_file_name='./data/data.csv',
    feature_columns_list=[
        'age',
        'anaemia',
        'creatinine_phosphokinase',
        'diabetes',
        'ejection_fraction',
        'high_blood_pressure',
        'platelets',
        'serum_creatinine',
        'sex',
        'smoking'
    ],
    label_columns_list=['DEATH_EVENT'],
    train_size=args.train_size,
    validation_size=args.validation_size
)
dataset_extractor.extract_dataset()
features_shape = dataset_extractor.get_features_shape()

# Extract the dataset split seeds.
dataset_split_seed_extractor = SeedExtractor(
    seeds_file_name='./data/seeds.csv',
    seeds_column_name='seed'
)
dataset_split_seed_extractor.extract_seeds()
dataset_split_seeds = dataset_split_seed_extractor.get_seeds()

# model = KerasSequential(
#     layers=[
#         Input(shape=features_shape),
#         Dense(400, activation='relu'),
#         Dense(20, activation='relu'),
#         Dense(1, activation='sigmoid')
#     ]
# )

# model = RandomForest(
#     criterion='gini',
#     max_depth=None,
#     max_features='sqrt',
#     max_leaf_nodes=None,
#     min_samples_leaf=1,
#     min_samples_split=2,
#     n_estimators=10
# )

# Define the models.
models = []

# for first_layer in range(100, 501, 100):
#     models.append(KerasSequential(
#         layers=[
#             Input(shape=features_shape),
#             Dense(first_layer, activation='relu'),
#             Dense(1, activation='sigmoid')
#         ]
#     ))

for n_estimators in range(100, 501, 100):
    models.append(RandomForest(
        criterion='gini',
        max_depth=None,
        max_features='sqrt',
        max_leaf_nodes=None,
        min_samples_leaf=1,
        min_samples_split=2,
        n_estimators=10
    ))

# Create model evaluator.
model_evaluator = ModelEvaluator(
    dataset_extractor=dataset_extractor,
    seed_list=dataset_split_seeds,
    models=models,
    num_validation_runs=20,
    num_test_runs=100,
    percent_of_models_tested=0.2,
    evaluation_number=1
)

model_evaluator.evaluate_models()
model_evaluator.print_results()
model_evaluator.save_results_as_csv()