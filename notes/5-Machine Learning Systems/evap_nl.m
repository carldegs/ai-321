load datasets;
 
%% Convert data sets into cell arrays for NARX
% Let X1 = inputs (u) and T1 = outputs (y) of Training Set
X1 = tonndata(train(:,1:3),false,false);
T1 = tonndata(train(:,4:6),false,false);
 
% Let X2 = inputs (u) and T2 = outputs (y) of Training Set
X2 = tonndata(valid(:,1:3),false,false);
T2 = tonndata(valid(:,4:6),false,false);
 
%% Train a NARX using [X1,T1] (Training)
inputDelays = 1:2;                          % No. of lags in u
feedbackDelays = 1:2;                       % No. of lags in y
hiddenLayerSize = 12;                       % No. of hidden neurons
 
net = closeloop(narxnet(inputDelays,...
    feedbackDelays,hiddenLayerSize));       % Set architecture
 
% You can change how the data set is divided:
net.divideParam.trainRatio = 70/100;        % Training Data Size
net.divideParam.valRatio = 20/100;          % Validation Data Size
net.divideParam.testRatio = 10/100;         % Test Data Size
 
[x,xi,ai,t] = preparets(net,X1,{},T1);
net = trainbr(net,x,t,xi,ai);               % Set training algorithm
 
%% Test the NARX using [X2,T2] (Validation)
[x,xi,ai] = preparets(net,X2,{},T2);
Y = cell2mat(net(x,xi,ai))';
M = length(Y); L = length(valid);
fit = (1-goodnessOfFit(Y,valid((L-M+1):L,4:6),'NMSE'))*100;

%% Plot the results (NARX vs. Actual)
subplot(311);
plot(1:L,valid(:,4),'k'); hold on;
plot((L-M+1):L,Y(:,1),'b'); hold off;
 
subplot(312);
plot(1:L,valid(:,5),'k'); hold on;
plot((L-M+1):L,Y(:,2),'b'); hold off;
 
subplot(313);
plot(1:L,valid(:,6),'k'); hold on;
plot((L-M+1):L,Y(:,3),'b'); hold off;
legend('Actual Data','Predicted Data');
 
ylab = {'L2','P2','X2'};
for j = 1:length(fit)
    fprintf('Fit %s:\tR^2 = %.4f%%\n',ylab{j},fit(j));
end
fprintf('Average fit: R^2 = %.4f%%\n',mean(fit));