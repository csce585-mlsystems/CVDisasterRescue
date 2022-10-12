import matplotlib.pyplot as plt
import pandas as pd

validation_loss_dataframe = pd.read_csv('tensorboard_data/validation_loss_total_val.csv', usecols=['Step', 'Value'])
validation_loss_dataframe.plot(x='Step', y='Value', kind='line')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.title('Total Validation Loss')
plt.show()