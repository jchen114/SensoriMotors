close all; clc;

output_directory = '../Inverse Dynamics Output/';
input_directory = '../Motion Files/';

listings = dir(strcat(output_directory,'*.sto'));

downsample_factor = 3;

inputs = cell(1, length(listings));
outputs = cell(1, length(listings));

for listing = 1 : length(listings)
    %% Find the output files
    file_name = listings(listing).name;
    fid_o = fopen(strcat(output_directory, file_name));
    output_data = textscan(fid_o,'%f %f %f %f %f %f %f %f %f %f %f %f', 'Delimiter', 'Whitespace', 'HeaderLines', 7);
    output_data_mat = cell2mat(output_data);
    
    if (size(output_data_mat,1) > 99)
        output_data_mat = output_data_mat(1:99,:);
    end
    
    %% Find the corresponding input file
    [file_number, ~] = strtok(file_name,'.');
    fid_i = fopen(strcat(input_directory, file_number, '.mot'));
    input_data = textscan(fid_i,'%f %f %f %f %f %f %f %f %f %f %f %f', 'Delimiter', 'Whitespace', 'HeaderLines', 11);
    input_data_mat = cell2mat(input_data);
    
    if (size(input_data_mat,1) > 99)
        input_data_mat = input_data_mat(1:99,:);
    end
    
    fclose(fid_o);
    fclose(fid_i);
    
    %% Downsample 
    input_ds = input_data_mat(1:downsample_factor:size(input_data_mat,1), :);
    output_ds = output_data_mat(1:downsample_factor:size(output_data_mat,1),:);
    inputs{listing} = input_ds;
    outputs{listing} = output_ds;

end

clearvars -except inputs outputs

%% Create and train a neural network
num_inputs = size(inputs{1}, 1);
size_inputs = size(inputs{1}, 2);
network = create_neural_network(num_inputs, size_inputs, 5);
network = train_neural_network(network, inputs, outputs, 15, 2000);
