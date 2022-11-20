# CVDisasterRescue

## Project Proposal
The project proposal PDF document is linked [here.](/proposal/proposal.pdf)

## Milestones
Milestone materials can be found [here.](/milestones)
* [Milestone 1 Document](/milestones/milestone1.pdf)
* [Milestone 2 Document](/milestones/milestone2.pdf)

## Source
All working code and demonstration is found in the `src` folder.

## Build Notes
While the project can be run using the native webcam of a laptop or other such USB webcam and microphone array, for demonstration as well as building purposes, we have decided to use the PlayStation Eye accessory, which contains both a camera and microphone array in one.

In order to use the PlayStation Eye accessory, you will need to install the appropriate drivers and Python library [pseyepy](https://github.com/bensondaled/pseyepy).

All other dependencies are listed in `src/dependencies.txt` and can be installed simply using `pip install -r src/dependencies.txt`. Some of the dependencies may be large, and you may want them to be isolated. In that case, we recommend using a Python virtual environment in order to isolate installed dependencies from the rest of the system. 

