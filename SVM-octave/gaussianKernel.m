function sim = gaussianKernel(x1, x2, sigma)
%RBFKERNEL returns a radial basis function kernel between x1 and x2
%   sim = gaussianKernel(x1, x2) returns a gaussian kernel between x1 and x2
%   and returns the value in sim

x1 = x1(:); x2 = x2(:);

% You need to return the following variables correctly.
sim = 0;

sim = e ^ (-1 * sum((x1-x2).*(x1-x2)) / (2*sigma*sigma));
   
end
