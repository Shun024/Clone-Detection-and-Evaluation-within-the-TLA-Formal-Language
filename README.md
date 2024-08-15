# Clone Detection and Evaluation within the TLA+ Formal Language

This repository is associated with the project for clone detection and analysis within TLA+ specifications. In this repository, you can get access to collection of TLA+ collections, code for preprocessing, tokenization, clone detection, output statistics and visualisations. 

## Project Description

Supervisor: Marie Farrell

Difficulty: C

Formal methods can often lack some basic, and very useful, software engineering features such as dedicated modularisation constructs/capabilities. This project seeks to repeat our previous work [1] on specification clones for Event-B formal models but, rather than Event-B, will focus on an alternate formal method (e.g. CSP [2], TLA+ [3], Dafny [4], etc.). This will involve:
* choosing an appropriate formal method to examine
* defining what is meant by a "specification clone" in the chosen formal method
* extending the (python) clone detector developed in [1] to read and examine specifications in the chosen formal method
* examining the results, drawing comparisions with [1]
* potentially proposing modularisation features for the chosen formal method if appropriate
[1] Farrell, M., Monahan, R., & Power, J. F. (2017). Specification Clones: An empirical study of the structure of Event-B specifications. In Software Engineering and Formal Methods: 15th International Conference, SEFM 2017, Trento, Italy, September 4–8, 2017, Proceedings 15 (pp. 152-167). Springer International Publishing.
[2] Hoare, C. A. R. (1978). Communicating sequential processes. Communications of the ACM, 21(8), 666-677.
[3] Lamport, L. (2002). Specifying systems: the TLA+ language and tools for hardware and software engineers.
[4] Leino, K. R. M. (2010). Dafny: An automatic program verifier for functional correctness. In Logic for Programming, Artificial Intelligence, and Reasoning: 16th International Conference, LPAR-16, Dakar, Senegal, April 25–May 1, 2010, Revised Selected Papers 16 (pp. 348-370). Springer Berlin Heidelberg.

Difficulty key
* C = Challenging
* H = Hard
* F = Flexible
* M = Moderate
* S = Straight forward
* N = Not suitable

## Project Details



### Report
[Report.pdf](https://github.com/Shun024/Clone-Detection-and-Evaluation-within-the-TLA-Formal-Language/blob/main/Report.pdf)
### Software Architecture Diagram

![architecture desgin diagram](https://github.com/Shun702/Final-Year-Project/blob/e6ca42eb4133848b018167f5c613897631bc4e4e/Architecture%20design-2.png?raw=true)

### Functional Requirements & Validation

Functional requirements: [Requirement verification.pdf](https://github.com/Shun702/Final-Year-Project/files/14883008/Requirement.verification.pdf)

Validation: [Requirement verification-2.pdf](https://github.com/Shun702/Final-Year-Project/files/14883010/Requirement.verification-2.pdf)

## Code Base
### Pre-requisite

Make sure the following are installed before running

- Python (at least version 3)
- Matplotlib
- Pandas

### How to run me

run the following in the terminal:
```
$ python3 run_script.py
```
### Customizing

To run the repository with your own collection of TLA+, replace TLA+ files in 'files' folder with your collection of TLA+ files. Then, run the code. 
