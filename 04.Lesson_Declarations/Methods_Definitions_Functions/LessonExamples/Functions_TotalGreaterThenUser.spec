methods {
    getFunds(address) returns (uint256) envfree
    getTotalFunds() returns (uint256) envfree
    getEthBalance(address) returns (uint256);
}

function preFunctionCall(env e) returns bool {
    uint256 userFunds = getFunds(e.msg.sender);
	uint256 total = getTotalFunds();
    return total >= userFunds;
}

function callDeposit(env e, uint256 amount){
    deposit(e, amount);
}

function assetTotalGreaterThanSingle(uint256 total, uint256 userFunds){
    assert ( total >=  userFunds, "Total funds are less than a user's funds " );
}

rule totalFundsAfterDeposit(uint256 amount) {
	env e; 
	
    bool preCall = preFunctionCall(e);
    require preCall;
	
    callDeposit(e, amount);

	uint256 userFundsAfter = getFunds(e.msg.sender);
	uint256 totalAfter = getTotalFunds();
	
    assetTotalGreaterThanSingle(totalAfter, userFundsAfter);
    // This assert is here since the syntax checker expects an assert as the last line of a rule.
    // assert (true) will always pass.
    assert (true); // Comment this line out and look at the running error you get.
}


rule totalFundsAfterDepositWithPrecondition(uint256 amount) {
	env e; 
	
    bool preCall = preFunctionCall(e);
    
    require preCall;
	callDeposit(e, amount);

	uint256 userFundsAfter = getFunds(e.msg.sender);
	uint256 totalAfter = getTotalFunds();
	
    assetTotalGreaterThanSingle(totalAfter, userFundsAfter);
    // This assert is here since the syntax checker expects an assert as the last line of a rule.
    // assert (true) will always pass.
    assert (true); // Comment this line out and look at the running error you get.
}

