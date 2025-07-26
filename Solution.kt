class Solution {
    fun maxSubarrays(n: Int, conflictingPairs: Array<IntArray>): Long {
        // Find the first pair that contains n
        val filtered = conflictingPairs.firstOrNull { pair -> n in pair }
            ?: return 0L // If no pair contains n, return 0
        
        // Calculate the range length
        val rangeLength = kotlin.math.abs(filtered[1] - filtered[0]) + 1
        
        // Calculate number of subarrays using formula: n*(n+1)/2
        // This replaces the nested loops that generate all subarrays
        val numberOfSubarrays = (rangeLength.toLong() * (rangeLength + 1)) / 2
        
        return numberOfSubarrays
    }
}