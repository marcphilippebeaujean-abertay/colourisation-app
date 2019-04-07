class NetworkLayer:
    def __init__(self, output_dim, input_dim):
        self.input_dim = input_dim
        self.output_dim = output_dim

    def calculate_output(self):
        raise RuntimeError('output for layer cannot be calculated')

    def forward_pass(self, input):
        raise RuntimeError('forward pass for layer undefined')

    def backward_pass(self):
        raise RuntimeError('backward pass for layer undefined')

