pragma solidity ^0.4.24;

contract SummaryContract{
    address public ownerAddr;
    
    enum STATUS {DISABLE, ENABLE}
    
    struct SC{
        uint64 id_number;
        address ppr;
        STATUS stt;
    }
    SC sc;
    
    mapping(uint64 => SC) public PPR;
    
    modifier onlyOwner{
        require(msg.sender == ownerAddr);
        _;
    }
    
    constructor(address owner) public{
        ownerAddr = owner;
    }
    
    function newPPR(uint64 id_number, address ppr, STATUS stt) onlyOwner public{
        sc.id_number = id_number;
        sc.ppr = ppr;
        sc.stt = stt;
        
        PPR[id_number] = sc;
    }
    
    function changeStatus(uint64 id_number, STATUS stt) onlyOwner public{
        sc.id_number = PPR[id_number].id_number;
        sc.ppr = PPR[id_number].ppr;
        sc.stt = stt;
        
        PPR[id_number] = sc;
    }
    
    function getInfo(uint64 id_number) view public returns(address, STATUS){
        return (PPR[id_number].ppr, PPR[id_number].stt);
    }
}