# FF-Interface
Force-feedback human-machine interface for an endoscopic application

## Description
This is the code that goes along with the master thesis "Design of a force-feedback human machine interface for an endoscopic application".

## `main.py` 
Is obvisouly the main code. It uses the 3 svr_f\*2.joblib SVMs to run. There needs to be a localhost connection with port 2055 to the [iLLumiSense software](https://fbgs.com/components/illumisense-software/ "iLLumiSense") 

## `static_for_pictures.py`
Is simply a static version of the main code, that needs no connection nor SVMs. The force data is manually hardcoded and running the code simply outputs a visual representation of this data.

## `gui_dispatch.py`
Is a Graphical User Interface (GUI) that allows the user to tweak the details of the code and choose between different options. Clicking on "Launch !" runs `main.py` and thus requires the SVMs and connection.

