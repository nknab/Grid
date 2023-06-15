# Grid

#### Folder and File Structure
Factory
  - This folder contains all the codes for the robots.
  
Server
  - This folder contains all the codes for the server.
  
Web App
  - This folder contains all the codes for the Grid web application.
  
 grid.sql
  - This is the database structure for the project.


The challenge imitates the Ghana Textiles Printing (GTP) production process in three major stages: Design, Production and Delivery.
The raw material used in the challenge is the standard paper roll used for receipts, in the color white. The size of the paper used is 10.4 x 8 cm, making a single yard. Each yard is sequentially cut a number of times depending on the quantity ordered at the design stage of the process. At each stage, messages are communicated back and forth, using MQTT on a single broker (grid.local) with varying topics. Below is a high-level architecture of the interactions between the stages.
![alt text](https://i0.wp.com/nknab.com/wp-content/uploads/2022/12/HLA.png?w=939&ssl=1)

## DESIGN & PLANNING STAGE
The challenge is made up of different processes that make up the three major stages. The Design stage involves using drag and drop controls over a web application to create a design for the product as shown in 3, on the high-level architecture. Also, at this stage, a form to indicate the order details (name, quantity, depot) is filled out to start the production process. The information comprising of the product design and order details are stored on the database and fetched when needed. This is shown below:
![alt text](https://i0.wp.com/nknab.com/wp-content/uploads/2022/12/grid-labelled.png?w=937&ssl=1)

## PRODUCTION STAGE
The production stage involves the rolling, printing and cutting activities of the challenge in that order. The rolling and cutting are default processes whereas the printing forms part of the challenge. The challenge of printing involves two parts: Programming and MQTT Communication. In the printing stage, the idea is to use an X, Y, Z & Grabber print system to create a pattern based on a specific design.


## DELIVERY STAGE
The delivery stage involves two major activities: carrier transportation and depot delivery. Carrier transportation moves the full or empty crate, to either the drop-off or pick-up point, and this is a default process. The depot delivery that forms part of the challenge, involves the task of building a forklift for lifting the crate and using line-following to traverse the path, leading to the specific depot. The depot delivery challenge has three major activities: Building, Programming and MQTT Communication.
