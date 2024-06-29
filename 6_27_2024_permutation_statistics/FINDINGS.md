# Summary of findings.

## Statistic 1
**Accuracy achieved: 100%**

**Description of model weights: Using a very simple model with no hidden layers, a value of 0 is heavily negatively correlated with a 1 in the nth position, and a value of 1 is heavily positively correlated with a 1 in the nth position. Additionally, a 1 appearing anywhere else, or the nth position not being a 1 makes this stat less likely.**

**How to compute statistic: This stat is 1 exactly when the last digit is 1**


## Statistic 2
**Accuracy achieved: 100%**

**Description of model weights: Using a very simple model with no hidden layers, a value of 1 is more often predicted when 4 is large and 5 is small, with greater strength based on how large or small.**

**How to compute statistic: This stat is 1 exactly when the 2nd to last digit is greater than the last digit**


## Statistic 3
**Accuracy achieved: 100%**

**Description of model weights: Honestly looks completely random. D:**

**How to compute statistic: See above**

## Statistic 4
**Accuracy achieved: 100%**

**Description of model weights: Only the first two hidden features were used with any significance, so it's not unlikely that hidden features were not needed. Both of these features were highly positively correlated with position 1 containing a 1, position 2 containing a 2, and so on. Additionally, these features were highly negatively correlated with this statistic being a 1.**

**How to compute statistic: This stat is 0 exactly when any digit's value matches its position (with 1-indexing)**

## Statistic 5
**Accuracy achieved: 100%**

**Description of model weights: To just interpret the model, I used a simple model with no hidden layers, though I had to add a hidden layer with many features to increase accuracy, at the cost of interpretability. For this reason, I will explain the weights on the version without a hidden layer: Most notably a value of 0 was achieved with near 100% certainty when the digits were least to greatest, and a value of (n)(n-1)/2 was achieved with near 100% certainty when the digits were greatest to least. Additionally, for predicting values other than the minimum or maximum possible value, the highly positively correlated connections would kind of "spread out" the more you stray from one of the extrema, also losing some certainty.**

**How to compute statistic: Create a running sum initialized to 0. For each digit, then for each digit to its right, if it is larger than that digit to its right, add 1 to the sum (e.g. For 12543, 5 is larger than 4 and 3, and 4 is larger than 3, so this stat will have value 3). This can be thought of as a measure of how far away the list is from being sorted from smallest to largest.**

## Statistic 6
**Accuracy achieved: 100%**

**Description of model weights: Admittedly, I can't entirely tell what's going on with these weights. Given that I could already tell the stat seemed to be closely related to stat 5, I was hoping that adding a layer similar to what I used to figure out stat 5 would give me weights I could interpret similarly well as I got for stat 5, though this was not the case.**

**How to compute statistic: Simply take stat5 % 2. Or, more intuitively, if stat5 is even, stat6 is 0, and if stat5 is odd, stat6 is 1.**

## Statistic 7
**Accuracy achieved: 97.2%**

**Description of model weights: Again, despite the similarity to stat5, I really can't figure out how to interpret the weights here.**

**How to compute statistic: Also similar to stat5, though not in the same way as stat6 is similar to stat5. This stat is simply the number of digits that are larger than the digit immediately to their right, instead of considering all digits to the right of each digit.**

## Statistic 8
**Accuracy achieved: 98.8%**

**Description of model weights: Not sure D:**

**How to compute statistic: Not sure D:**

## Statistic 9
**Accuracy achieved: 97.9%**

**Description of model weights: Not sure. This looks vaguely similar to stat8, though that may just be because I copied all of the settings from there.**

**How to compute statistic: Not sure D:**