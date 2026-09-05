This file contains antimicrobial susceptibility testing (AST) records for Escherichia coli derived from the Bacterial and Viral Bioinformatics Resource Center (BV-BRC; formerly PATRIC). The dataset was used as the phenotypic source for generating the resistant/susceptible (R/S) classification targets and quantitative minimum inhibitory concentration (MIC) regression targets in the study.Each row represents an antibiotic-specific AST record associated with an E. coli genome/isolate. A genome may therefore occur in multiple rows because multiple antibiotics and/or measurements may be available for the same genome.

**Data source**

* Source: Bacterial and Viral Bioinformatics Resource Center (BV-BRC; formerly PATRIC)
* Organism: Escherichia coli
* Data type: Antimicrobial susceptibility testing (AST), including R/S phenotype and MIC measurements
* File type: Tab-delimited text file (.txt)

**Dataset size**

* Total lines: 155,014
* AST records: 155,013 (excluding the header)
* Columns: 16

**Column	Description**

* genome_id:	Unique BV-BRC/PATRIC genome identifier
* genome_name:	Genome/isolate name
* taxon_id:	Taxonomic identifier
* antibiotic:	Antibiotic tested
* resistant_phenotype:	Reported resistance/susceptibility phenotype
* measurement:	Original AST measurement
* measurement_sign:	Measurement qualifier, such as <= or >
* measurement_value:	Numeric component of the measurement
* measurement_unit:	Measurement unit, e.g. mg/L
* laboratory_typing_method:	Laboratory AST method, e.g. MIC
* laboratory_typing_method_version:	Version of the laboratory method, when available
* laboratory_typing_platform:	Testing platform, when available
* vendor:	Vendor information, when available
* testing_standard:	Testing/interpretation standard, e.g. CLSI
* testing_standard_year:	Year of the testing standard
* source:	Source information, when available
