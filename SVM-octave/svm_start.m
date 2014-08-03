%% Initialization
clear ; close all; clc

fprintf('Program paused. Press enter to continue.\n');
pause;

load('svmTrain.txt');

fprintf('\nTraining Linear SVM for Classification\n')
fprintf('(this may take 1 to 2 minutes) ...\n')

C = 0.1;
% C parameter is a positive value that
% controls the penalty for misclassified training examples. A large C parameter
% tells the SVM to try to classify all the examples correctly. C plays a role
% similar to 1/λ , where λ is the regularization parameter that we were using
% previously for logistic regression.

% For linear decision boundaries
% model = svmTrain(X, y, C, @linearKernel);

% For non-linear decision boundaries
model = svmTrain(X, y, C, @gaussianKernel);

p = svmPredict(model, X);
fprintf('Training Accuracy: %f\n', mean(double(p == y)) * 100);

% Load the test dataset
load('svmTest.txt');

fprintf('\nEvaluating the trained Linear SVM on a test set ...\n')

p = svmPredict(model, Xtest);

fprintf('Test Accuracy: %f\n', mean(double(p == ytest)) * 100);
pause;
