import pybrain
from pybrain.structure import RecurrentNetwork, FullConnection, LinearLayer, SigmoidLayer
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
#ginsem library

#Define network structure
network = RecurrentNetwork(name="XOR")

inputLayer = LinearLayer(2, name="Input")
hiddenLayer = SigmoidLayer(3, name="Hidden")
outputLayer = LinearLayer(1, name="Output")

network.addInputModule(inputLayer)
network.addModule(hiddenLayer)
network.addOutputModule(outputLayer)

c1 = FullConnection(inputLayer, hiddenLayer, name="Input_to_Hidden")
c2 = FullConnection(hiddenLayer, outputLayer, name="Hidden_to_Output")
c3 = FullConnection(hiddenLayer, hiddenLayer, name="Recurrent_Connection")

network.addConnection(c1)
network.addRecurrentConnection(c3)
network.addConnection(c2)

network.sortModules()

#Add a data set
ds = SupervisedDataSet(2,1)


ds.addSample([1,1],[0])
ds.addSample([0,0],[0])
ds.addSample([0,1],[1])
ds.addSample([1,0],[1])

#Train the network
trainer = BackpropTrainer(network, ds, momentum=0.99)

print network

print "\nInitial weights: ", network.params

max_error = 1e-7
error, count = 1, 1000
#Train
while abs(error) >= max_error and count > 0:
    error = trainer.train()
    count = count - 1

print "Final weights: ", network.params
print "Error: ", error

#Test data
print '\n1 XOR 1:',network.activate([1,1])[0]
print '1 XOR 0:',network.activate([1,0])[0]
