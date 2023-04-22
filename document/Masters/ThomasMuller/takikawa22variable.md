## Paper:10




1. Title: Variable Bitrate Neural Fields

2. Authors: Towaki Takikawa, Alex Evans, Jonathan Tremblay, Thomas Müller, Morgan McGuire, Alec Jacobson, Sanja Fidler

3. Affiliation: Towaki Takikawa is affiliated with NVIDIA and the University of Toronto, Canada

4. Keywords: neural fields, feature grids, machine learning, compression, out-of-core streaming

5. Urls: https://dl.acm.org/doi/10.1145/3528233.3530727

Github: https://github.com/nv-tlabs/vqad

6. Summary:

- (1): This article explores methods to reduce the memory consumption of feature grids in neural fields, which are commonly used for tasks such as view synthesis and signal reconstruction. The authors aim to provide a more efficient and scalable method for these tasks.

- (2): Previous methods for feature grids have been effective, but they come at a significant cost in terms of memory consumption. The authors propose a dictionary method for compressing feature grids, which can reduce their memory consumption by up to 100 times. This allows for a multiresolution representation that can be used for out-of-core streaming. The approach is well-motivated by the need for more efficient and scalable methods for neural fields.

- (3): The proposed methodology involves formulating the dictionary optimization problem as a vector-quantized auto-decoder problem. This allows for the learning of end-to-end discrete neural representations in a space where no direct supervision is available, and with dynamic topology and structure.

- (4): The methods proposed in this paper are evaluated on tasks related to radiance fields and signed distance functions, and achieve competitive performance compared to previous methods while consuming significantly less memory. The performance supports the authors' goals of providing a more efficient and scalable method for neural fields.
7. Methods: 

- (1): 本文提出了一种压缩神经场中特征网格的方法，其目的是减少其内存消耗。该方法在视图合成和信号重建等任务中经常使用，并提供了更高效和可扩展的方法。

- (2): 在之前的特征网格方法中，其对内存的消耗较高，本文提出了基于词典的压缩方法，可将内存消耗降低100倍。该方法具有多分辨率表示，可用于外部存储流式处理，并能更好地实现压缩表示。

- (3): 根据所提出的方法，将词典的优化问题制定为向量量化自编码器的问题。这种方法允许在没有直接辅助的情况下，在动态拓扑和结构的空间中学习端到端的离散神经表示。

- (4): 本文提出的方法在辐射场和符号距离函数等任务上进行了评估，与先前的方法相比，在消耗更少的内存情况下具有竞争性的性能。这一结果支持了我们提出的方法提供更高效和可扩展的神经场方法的目标。





8. Conclusion: 

- (1): 本文的意义在于提出了一种压缩神经场中特征网格的方法，能够更高效和可扩展地实现视图合成和信号重建等任务。

- (2): 创新点：本文提出了基于词典和向量量化自编码器的压缩方法，可以将内存消耗降低100倍，实现外部存储流式处理和更好的压缩表示；性能：实现了与先前方法相比在消耗更少的内存情况下具有竞争性的性能；工作量：该方法在训练时需要的内存和计算量较大，但这可以通过混合随机和学习的方式来改善。因此，该方法具有一定的局限性。




