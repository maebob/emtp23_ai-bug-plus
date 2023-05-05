# European Master Team Project: AI BugPlus
> This repository contains the developed code of the AI BugPlus team project during the fall semester 2022 and the spring semester 2023.
> The project was supervised by [Dr. Christian Bartelt](https://www.uni-mannheim.de/en/ines/about-us/researchers/dr-christian-bartelt/) and [Jannik Brinkmann](https://www.linkedin.com/in/brinkmann-jannik/) at the [University of Mannheim](https://www.uni-mannheim.de/), Germany and took place in cooperation with [Babeș-Bolyai University](https://www.ubbcluj.ro/en/) in Cluj Napoca, Romania.

## Introduction

The language BugPlus can be used to solve logical Problems by placing and connection so called Bugs on a board. Because BugPlus is Turing complete, technically any mathematical function can be solved. This means that teaching an agent how to solve given problems using BugPlus is comparable to teaching an agent how to write code given a problem specification.

Using the approach described above, we used Reinforcement Learning techniques to train agents to solve a restricted class of problems in BugPlus. To do so an abstracted version of a BugPlus board has been used as a training environment.

In order to build out problems and possible configurations in BugPlus, we discovered a need for a visual editor. This is why we also created a publicly accessible editor for BugPlus.

## Participants

### Babeș-Bolyai University

* [Radu Tarean](https://github.com/2XG-DEV) - B.Sc. Computer Science
* [Rares Martisan](https://github.com/rares9991) - B.Sc. Computer Science

### University of Mannheim

* [Aaron Steiner](https://github.com/Aaron9812) - M.Sc. Data Science
* [Mae Turner](https://github.com/maebob) - M.Sc. Data Science
* [Mayte Dächer](https://github.com/misssophieexplores) - M.Sc. Data Science

## Repository Structure
| Folder | Content |
| :-- | :-- |
| docs | Folder to generate the documentation |
| gamification | Manual and challenges for a gamified version of BugPlus |
| heuristics | Configs for all possible problems that can be solved using three bugs |
| result_logging | Analysis of train logs |
| src | Environment, agents, evaluation engine and generator for training data |
| tests | Tests for the evaluation engine |
| wandb | Run information for Weights & Biases |

## Weights and Biases

## BugPlus Editor
Here you can find the link to our BugPlus Editor:
[![editor](https://user-images.githubusercontent.com/55137042/235347194-46dbea7d-e141-44f9-b463-9dfe53eb4ff8.png)](https://bug-plus-web-app.vercel.app/challenges/Incrementor)


## Create the Docker Container 
```console
foo@bar:~$ docker build -t ![Uploading editor.png…]()
bugapi . 
foo@bar:~$ docker run -d --name bug_api -p 90:80 bugapi
```

## Final Presentation
Here you can find the link to our final presentation:
[![emtp23_final_presentation_cover_slide](https://user-images.githubusercontent.com/55137042/236400140-666e5edc-3548-47e6-9ea0-45d920a7cca4.png)](https://github.com/maebob/emtp23_ai-bug-plus/blob/d1cc76ce80db8c0c86b2ec704cd6189c941e7d1c/emtp23_final_presentation.pdf)

## Setting Environment Variables

This project requires certain environment variables to be set before running. An example of the required environment variables can be found in the `.env.example` file.

To set the environment variables:

1. Make a copy of the `.env.example` file and name it `.env`:

```bash
cp .env.example .env
```


2. Open the `.env` file in your preferred text editor and replace the placeholder values with your actual configuration values.

3. Save the `.env` file.

Remember to set the environment variables in each environment where the project will be run, such as development, testing, and production.
