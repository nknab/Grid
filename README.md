# Grid

The challenge imitates the Ghana Textiles Printing (GTP) production process in three major stages: Design, Production and Delivery.
The raw material used in the challenge is the standard paper roll used for receipts, in the color white. The size of the paper used is 10.4 x 8 cm, making a single yard. Each yard is sequentially cut a number of times depending on the quantity ordered at the design stage of the process. At each stage, messages are communicated back and forth, using MQTT on a single broker (grid.local) with varying topics. Below is a high-level architecture of the interactions between the stages.
