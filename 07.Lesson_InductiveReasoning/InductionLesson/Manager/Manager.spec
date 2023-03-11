methods {
	getCurrentManager(uint256 fundId) returns (address) envfree
	getPendingManager(uint256 fundId) returns (address) envfree
	isActiveManager(address a) returns (bool) envfree
}



rule uniqueManagerAsRule(uint256 fundId1, uint256 fundId2, method f) {
	// assume different IDs
	require fundId1 != fundId2;
	// assume different managers
	require getCurrentManager(fundId1) != getCurrentManager(fundId2);
	
	// hint: add additional variables just to look at the current state
	// bool active1 = isActiveManage(getCurrentManager(fundId1));

	require getCurrentManager(fundId1) != 0 => isActiveManager(getCurrentManager(fundId1));
	require getCurrentManager(fundId2) != 0 => isActiveManager(getCurrentManager(fundId2));
	
	env e;
	calldataarg args;

	if (f.selector == claimManagement(uint256).selector || 
			f.selector == createFund(uint256).selector || 
			f.selector == setPendingManager(uint256, address).selector) 
	{
		require !isActiveManager(e.msg.sender);
	}
	f(e,args);
	
	// verify that the managers are still different 
	assert getCurrentManager(fundId1) != getCurrentManager(fundId2), "managers not different";
}

 /* A start of uniqueManagerAsRule as an invariant, we will see in next lecture how to prove this */


invariant uniqueManagerAsInvariant(uint256 fundId1, uint256 fundId2)
	fundId1 != fundId2 => getCurrentManager(fundId1) != getCurrentManager(fundId2) 
