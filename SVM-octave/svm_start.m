%% Initialization
clear ; close all; clc

fprintf('Program paused. Press enter to continue.\n');
pause;

load('svmTrain.txt');

fprintf('\nTraining Linear SVM for Classification\n')
fprintf('(this may take 1 to 2 minutes) ...\n')

C = 0.1;
% model = svmTrain(X, y, C, @linearKernel);
model = svmTrain(X, y, C, @gaussianKernel);

p = svmPredict(model, X);
fprintf('Training Accuracy: %f\n', mean(double(p == y)) * 100);

% Load the test dataset
load('svmTest.txt');

fprintf('\nEvaluating the trained Linear SVM on a test set ...\n')

p = svmPredict(model, Xtest);

fprintf('Test Accuracy: %f\n', mean(double(p == ytest)) * 100);
pause;
