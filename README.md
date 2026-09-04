# E.Coli_AMR_PanGenome_ML

**Overview**

This repository contains the computational workflows, analysis scripts, and reproducibility resources for a pan-genome-based machine learning study of antimicrobial resistance (AMR) phenotypes and minimum inhibitory concentration (MIC) prediction in Escherichia coli.

The study integrates whole-genome protein sequence information, pan-genome analysis, antimicrobial susceptibility testing (AST) data, feature selection, and machine learning to identify compact sets of genomic features associated with antimicrobial resistance phenotypes and quantitative MIC values.

The computational framework includes both:

R/S classification :prediction of resistant (R) and susceptible (S) phenotypes.
MIC regression :prediction of quantitative MIC values.

The overall workflow is designed to identify predictive and biologically interpretable genomic determinants while reducing the dimensionality of the pan-genome feature space.

**The primary objectives of this study are to:**

* Construct a protein-level pan-genome of E. coli isolates.
* Integrate pan-genome features with antimicrobial susceptibility testing data.
* Develop machine learning models for AMR classification and MIC prediction.
* Identify a compact set of predictive genomic features through feature selection.
* Evaluate the effect of feature-reduction thresholds on predictive performance.
* Identify common genetic determinants selected independently from classification and regression tasks.
* Investigate those shared features between quantitative MIC prediction and categorical AMR classification.

**Data Source**

Genomic and antimicrobial susceptibility testing data were obtained from the Bacterial and Viral Bioinformatics Resource Center (BV-BRC; formerly PATRIC).

The analysis uses E. coli genome records together with corresponding antimicrobial susceptibility testing information.

**Dataset Processing**

The study dataset underwent multiple filtering and quality-control steps before pan-genome construction and machine learning.

The finalized genome collection contains qualified E. coli genomes with corresponding protein FASTA files.

The preprocessing workflow includes:

* Retrieval of genome metadata.
* Identification of unique genome records.
* Verification of available protein FASTA files.
* Removal of unsuitable or incomplete records.
* Integration of genomic and AST metadata.
* Selection of genomes satisfying the study-specific quality criteria.

The exact filtering criteria and processing procedures are implemented in the corresponding scripts in the scripts/ directory.

**Machine Learning Framework**

The computational workflow uses machine learning for two complementary prediction tasks.

1. AMR Classification

Classification models are used to predict:

Resistant / Susceptible

Performance is evaluated using multiple classification metrics, including:

* Accuracy
* AUROC
* Precision
* Recall
* F1-score
* Matthews correlation coefficient (MCC)
  
2. MIC Regression

Regression models are used to predict normalized quantitative MIC values.

Regression performance is evaluated using:

* Mean squared error (MSE)
* Mean absolute error (MAE)
* R-squared (R²)
* Pearson correlation coefficient
* Corresponding statistical significance measures where applicable

**XGBoost Modeling**

XGBoost is used as a major machine learning framework for both prediction tasks.

The implementation includes:

* XGBClassifier for AMR classification.
* XGBRegressor for MIC regression.

The main model configuration used in the study includes:

n_estimators = 100
max_depth = 6
random_state = 42
n_jobs = 8

Additional regularization parameters and model-specific settings are documented in the relevant scripts.


**Software Requirements**

The analysis was performed using Python-based scientific computing and machine learning tools.

Major software dependencies include:

* Python
* pandas
* NumPy
* scikit-learn
* XGBoost
* Matplotlib
* seaborn
* SciPy

Pan-genome construction additionally uses:

* CD-HIT

**Computational Resources**

The computational analyses were performed using a Linux-based computational environment.

Parallel processing was configured to use up to:

8 CPU cores

where supported by the implemented machine learning workflows.
