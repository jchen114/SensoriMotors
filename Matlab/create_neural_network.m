function [network] = create_neural_network(num_inputs, size_input, layers)
    % layers includes input, output, and hidden layers
    % Assume hidden layer have the same number of neurons as num_inputs
    % Initialize random weights and biases for the network.
    for layer = 1 : layers-1 % Minus the output layer
        for node = 1 : num_inputs
            network.layers{layer}.weights{node} = rand(num_inputs, size_input);
            network.layers{layer}.biases{node} = rand(1, size_input);
        end
    end
    
    network.input_size = size_input;
    network.number_of_layers = layers;
    network.hidden_layer_size = num_inputs;

end

