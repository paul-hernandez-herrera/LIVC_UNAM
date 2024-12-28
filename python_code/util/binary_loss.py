import torch

class BinaryLoss(torch.nn.Module):
    def __init__(self, option = 'dice', mode_single = True):
        self.option = option
        self.mode_single = mode_single
        super().__init__()
        
    def forward(self, model_output, target):
        # this function computer the dice loss function for two tensor. 
        # It assumes that model_output and target are of the same size [B, C, W, H]
        # We assume that the model returns the is not normalized to probabilities [0,1].
        
        # Normalizing to [0,1]
        #output = torch.sigmoid(model_output)
               
        if self.option == 'recall':
            # conditional probability --- P(ground_true|prediction)
            loss = self.general_equation(model_output, target, 0, 1, 1)
        elif self.option == 'precision':
            # conditional probability --- P(prediction|ground_true)
            loss = self.general_equation(model_output, target, 1, 0, 1)            
        elif self.option == 'kulczynski_I':
            loss = self.general_equation(model_output, target, 1, 1, 0)            
        elif self.option == 'dice':
            loss = self.general_equation(model_output, target, 1/2, 1/2, 1)
        elif self.option == 'sw_jaccard':
            loss = self.general_equation(model_output, target, 1/3, 1/3, 1)
        elif self.option == 'jaccard':
            loss = self.general_equation(model_output, target, 1  , 1  , 1)            
        elif self.option == 'sokal_and_sneath_I':
            loss = self.general_equation(model_output, target, 2  , 2  , 1)
        elif self.option == 'Van_der_Maarel':
            loss = 2*self.general_equation(model_output, target, 1/2, 1/2, 1) -1            
        elif self.option == 'johnson':
            loss = self.general_equation(model_output, target, 1, 0, 1) + self.general_equation(model_output, target, 0, 1, 1)
        elif self.option == 'mcconaughey':
            loss = self.general_equation(model_output, target, 1, 0, 1) + self.general_equation(model_output, target, 0, 1, 1) -1
        elif self.option == 'kulczynski_II':
            loss = (self.general_equation(model_output, target, 1, 0, 1) + self.general_equation(model_output, target, 0, 1, 1) ) / 2
        elif self.option == 'sorgenfrei':
            loss = self.general_equation(model_output, target, 1, 0, 1) * self.general_equation(model_output, target, 0, 1, 1)
        elif self.option == 'driver_kroeber_ochiai':
            loss = (self.general_equation(model_output, target, 1, 0, 1) * self.general_equation(model_output, target, 0, 1, 1)).sqrt()
        elif self.option == 'braun_blanquet':
            loss = torch.minimum(self.general_equation(model_output, target, 1, 0, 1), self.general_equation(model_output, target, 0, 1, 1))
        elif self.option == 'simpson':
            loss = torch.maximum(self.general_equation(model_output, target, 1, 0, 1), self.general_equation(model_output, target, 0, 1, 1))
            
        # goal minimize the metric. Dice best performance is at maximum value equal to one, then substracting one
        return 1-loss  
    
    def compute_conditional_probability(self, model_output, target):
        """
        Compute the conditional probability for each image in the batch and each channel.
        Conditional probability is computed independently for each image and channel.

        Args:
            model_output (torch.Tensor): Model predictions with shape [B, C, D1, D2, ..., DN].
            target (torch.Tensor): Ground truth labels with shape [B, C, D1, D2, ..., DN].

        Returns:
            torch.Tensor: Mean conditional probability across all images and channels.
        """
        if self.mode_single:
            N_dim = 0
        else:
            N_dim = 2
        # Determine the dimensions to reduce (spatial dimensions only: D1, D2, ..., DN)
        reduce_dims = tuple(range(N_dim, target.ndimension()))

        # Calculate the intersection between the model output and target
        intersection = (model_output * target).sum(dim=reduce_dims)

        # Calculate the total number of target elements (cardinality of the target)
        target_cardinality = target.sum(dim=reduce_dims)

        # Compute conditional probability: P(intersection | target)
        # Shape: [B, C], where B = batch size, C = number of channels
        conditional_prob = intersection / target_cardinality

        # Mask out cases where there is no foreground in the target (target cardinality is zero)
        valid_mask = target_cardinality != 0  # Create a mask where the cardinality is non-zero

        # Apply the mask to retain only valid values
        valid_conditional_prob = conditional_prob[valid_mask]

        # If all values are masked out, ensure you don't perform a mean on an empty tensor
        if valid_conditional_prob.numel() > 0:
            return valid_conditional_prob.mean()
        else:
            return torch.tensor(0.0, device=conditional_prob.device)  # Return zero if no valid values exist

        
    def general_equation(self, A, B, alpha, beta, gamma):
        if [alpha,beta,gamma]==[1,0,1]:
            return self.compute_conditional_probability(A, B)
        elif [alpha,beta,gamma]==[0,1,1]:
            return self.compute_conditional_probability(B, A)        
        else:
            Prob_A_B = self.compute_conditional_probability(A, B)
            Prob_B_A = self.compute_conditional_probability(B, A)        
            return 1/((alpha*((1/Prob_A_B)-1) ) + (beta*((1/Prob_B_A)-1) ) + gamma)
    
       