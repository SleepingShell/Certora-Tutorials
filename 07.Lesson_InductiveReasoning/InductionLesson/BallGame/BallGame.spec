
methods {
	ballAt() returns uint256 envfree
}

invariant neverReachPlayer4() 
	ballAt() != 4 && ballAt() != 3

rule parametric_neverReachPlayer4() {
	method f;
	env e;
	calldataarg arg;

	require ballAt() !=4 && ballAt() != 3;
	f(e, arg);

	assert ballAt() != 4;
}