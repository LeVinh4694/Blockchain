pragma solidity ^0.4.24;

contract RegistrarContract{
    address ownerAddr;
    
    struct RC{
        uint64 id_number;
        address accAddr;
        address RContract;
    }
    RC rc;
    
    mapping(uint64 => RC) public users;
    
    modifier onlyOwner{
        require(msg.sender == ownerAddr);
        _;
    }
    
    constructor() public{
        ownerAddr = msg.sender;
    }
    
    function newRecord(uint64 id_number, address accAddr, address RContract) onlyOwner public{
        rc.id_number = id_number;
        rc.accAddr = accAddr;
        rc.RContract = RContract;
        
        users[id_number] = rc;
    }
    
    function getInfo(uint64 id_number) public view returns(address, address){
        return (users[id_number].accAddr, users[id_number].RContract);
    }
}