David Duggan
CSCE 585
Dr. Jamshidi
September 7, 2022
# Assignment 1

## 1-	How many models do they deploy in parallel? Also, mention the type of models, e.g., Deep-NN. Decision trees?
While Lyft does not explicitly say how many models they deploy in parallel, the backbone of their service is run by Machine Learning. The estimated cost of a ride, whether a driver can cancel, route matching, driver/rider matching, and fraud detection are some examples of ML powered services that Lyft offers [1]. Lyft doesn’t explicitly disclose the types of models they use, but some of their projects give a hint. For example, Level 5 is Lyft’s self-driving team, and they use Computer Vision (Deep CNNs) and other models to create autonomous vehicles. Lyft also created their own gradient-boosted tree package, indicating that they use gradient-boosted trees.

## 2-	What ecosystem/framework/tools do they use for model deployment?
Lyft created its own cloud-native machine learning and data processing platform known as Flyte. “The platform executes complex workflows such as hardware provisioning, scheduling, data storage and monitoring for Lyft.” [1]. Lyft also uses AWS to detect anomalies and for Anodot, their AI-powered time-series analytics solution [1]. Lyft uses a fully distributed internal framework built on PyTorch, called Jadoo [2].

## 3-	How do they load balance between the models?
Lyft uses Kafka in serving their models, and thus, builds their load-balancing on Kafka. Lyft uses the built-in load balancer with Kafka and uses tags on their containers that are the same as Kafka’s built-in tags. This way, the Kafka load balancer will balance their loads [3].

## 4-	How do they retire a model?
Lyft does not disclose their model retirement process. However, considering Lyft’s commitment to innovation and the amount of ML they use, its safe to predict that they have an efficient method of retiring models. If they did not, users would notice problems when a model is retired.

## 5-	How do they update a model? On what regularity do they update the models? Only what matters regarding model deployment, not about model training.
Lyft does not disclose how they update their models, but given that much of their data is seasonal (such as when people are riding most) they likely update their models very often. This report shows how they deal with seasonality in their dataset, but does not specifically cover how/how regularly they update their ML models [4].

## 6-	What metrics do they use to monitor a model's performance and health?
LyftLearn serving takes prediction scores from the model and performs time-series computation to create time-series alerts based on the data [5]. This system ensures that models are not outputting the same score over a period of time, which could indicate issues somewhere.

## 7-	How long does it take for them to deploy a single model? (Consider model size as a confounding factor)
Lyft operates using Continuous Deployment (CD) and have worked with other teams around the company to get them all using this model. Using this method, Lyft’s deployments now take around 45 minutes each [6]. I am not sure if this includes machine learning or only covers microservices, but I would think they would have similar deployment infrastructure.

## 8-	How do they decrease the cost of model deployment?
Lyft uses a few different techniques to decrease the cost of their model deployment.  First, after performing feature engineering, they parallelize model training on multiple low-cost machines to reduce time and cost. Using Apache Spark and Kubernetes, Lyft can perform large scale data processing at up to 90% less cost [7].

# References:
[1] https://analyticsindiamag.com/all-about-lyfts-ml-architecture/#:~:text=In%202020%2C%20Lyft%20open%20sourced,storage%20and%20monitoring%20for%20Lyft.

[2] https://medium.com/pytorch/how-lyft-uses-pytorch-to-power-machine-learning-for-their-self-driving-cars-80642bc2d0ae

[3] https://eng.lyft.com/building-an-adaptive-multi-tenant-stream-bus-with-kafka-and-golang-5f1410bf2b40

[4] https://eng.lyft.com/how-to-deal-with-the-seasonality-of-a-market-584cc94d6b75

[5] https://eng.lyft.com/full-spectrum-ml-model-monitoring-at-lyft-a4cdaf828e8f

[6] https://eng.lyft.com/continuous-deployment-at-lyft-9b457314771a

[7] https://www.databricks.com/dataaisummit/session/distributed-machine-learning-lyft#:~:text=Our%20ML%20platform%20is%20completely,rapid%20bootstrapping%20time%20of%20resources.
