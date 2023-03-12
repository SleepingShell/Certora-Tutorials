methods {
  getTokenAtIndex(uint256) returns (address) envfree
  getIdOfToken(address) returns (uint256) envfree
  getReserveCount() returns (uint256) envfree
  addReserve(address, address, address, uint256) envfree
  removeReserve(address) envfree
}

invariant listEntriesEqual(uint256 index, address token)
  (index != 0 && token != 0 => (getTokenAtIndex(index) == token <=> getIdOfToken(token) == index)) &&
   (index == 0 && token != 0 => (getTokenAtIndex(index) == token => getIdOfToken(token) == index))
  {
    preserved
    {
      requireInvariant indexLessThanCounter(token);
    }

    preserved removeReserve(address t) {
      require t == token;
    }
  }

invariant indexLessThanCounter(address token)
  (getReserveCount() > 0 => getIdOfToken(token) < getReserveCount()) && (getReserveCount() == 0 => getIdOfToken(token) == 0)
  {
    preserved removeReserve(address t) {
      require t == token;
    }
  }

invariant tokensHaveDistinctIds(address token1, address token2)
  token1 != token2 && token1 != 0 && token2 != 0 => (getIdOfToken(token1) == 0 || (getIdOfToken(token1) != getIdOfToken(token2)))
  {
    preserved
    {
      requireInvariant indexLessThanCounter(token1);
      requireInvariant indexLessThanCounter(token2);
      requireInvariant listEntriesEqual(getIdOfToken(token1), token1);
      requireInvariant listEntriesEqual(getIdOfToken(token2), token2);
    }
  }

rule tokenRemovalIndependence(address token, address other) {
  require token != other && token != 0 && other != 0;

  uint256 otherIdBefore = getIdOfToken(other);
  require otherIdBefore != 0;
  //require getTokenAtIndex(other) == otherIdBefore;

  requireInvariant tokensHaveDistinctIds(token, other);
  requireInvariant listEntriesEqual(otherIdBefore, other);
  //requireInvariant listEntriesEqual(getIdOfToken(token), token);

  removeReserve(token);

  uint256 otherIdAfter = getIdOfToken(other);
  address otherAddressAfter = getTokenAtIndex(otherIdAfter);

  assert otherIdBefore == otherIdAfter;
  assert other == otherAddressAfter;
}

rule nonViewChangesCount(method f) {
  uint256 countBefore = getReserveCount();

  env e;
  calldataarg args;
  f(e, args);

  uint256 countAfter = getReserveCount();
  assert !f.isView => countAfter - countBefore == 1 || countBefore - countAfter == 1;
}