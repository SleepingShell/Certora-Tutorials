# Valid States
createdState
startedState: started = true, endAt != 0, contract owns NFT
endedState: now() after endAt

all bids not highestBidder < highestBid

# State Transitions
Can only start if not already started or ended

# Variable Transitions
highestBid can only increase (New bid must be greater than the current highest bid)
highestBidder changes on valid bid()
Bids cannot occur after the auction window
setOperator correctly set

# High-Level Properties
sum of bids <= token.balanceOf(contract)

# Unit Tests
Everyone but current highest bidder can withdraw
end() correctly transfers both NFT and bid amount
withdrawFor operator is checked
ended=true iff end() is called while now() after endAt


NFT != 0
ERC20 != 0