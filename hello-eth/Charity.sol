pragma solidity >= 0.8.11 <= 0.8.11;
pragma experimental ABIEncoderV2;
//Charity solidity code
contract Charity {

    uint public userCount = 0; 
    mapping(uint => user) public userList; 
     struct user
     {
       string person_name;
       string phone;
       string email;
       string password;
       string user_type;
     }
 
   // events 
   event userCreated(uint indexed _userId);
   
   //function  to save user details to Blockchain
   function saveUser(string memory pname, string memory phone, string memory email, string memory pass, string memory ut) public {
      userList[userCount] = user(pname, phone, email, pass, ut);
      emit userCreated(userCount);
      userCount++;
    }

     //get user count
    function getUserCount()  public view returns (uint) {
          return  userCount;
    }

    uint public auctionCount = 0; 
    mapping(uint => auction) public auctionList; 
     struct auction
     {
       string auctioner_name;
       string auction_id;
       string auction_details;
       string minimum_amount;
       string start_date;
       string end_date;   
       string auction_category;       
     }
 
   // events 
   event auctionCreated(uint indexed _auctionId);
   
   //function  to save auction details to Blockchain
   function saveAuction(string memory aname, string memory aid, string memory ad, string memory ma, string memory sd, string memory edate, string memory cat) public {
      auctionList[auctionCount] = auction(aname, aid, ad, ma, sd, edate, cat);
      emit auctionCreated(auctionCount);
      auctionCount++;
    }

    //get auction count
    function getAuctionCount()  public view returns (uint) {
          return  auctionCount;
    }

    uint public bidCount = 0; 
    mapping(uint => bid) public bidList; 
     struct bid
     {
       string auction_id;
       string bidder;
       string amount;
       string bid_date;
       string transaction_type;
     }
 
   // events 
   event bidCreated(uint indexed _bidId);
   
   //function  to save Bidding details to Blockchain
   function saveBid(string memory aid, string memory bidder_name, string memory bid_amount, string memory bidding_date, string memory ttype) public {
      bidList[bidCount] = bid(aid, bidder_name, bid_amount, bidding_date, ttype);
      emit bidCreated(bidCount);
     bidCount++;
    }

     //get bid count
    function getBidCount()  public view returns (uint) {
          return  bidCount;
    }


    function getPersonname(uint i) public view returns (string memory) {
        user memory doc = userList[i];
	return doc.person_name;
    }

    function getPassword(uint i) public view returns (string memory) {
        user memory doc = userList[i];
	return doc.password;
    }

    function getPhone(uint i) public view returns (string memory) {
        user memory doc = userList[i];
	return doc.phone;
    }    

    function getEmail(uint i) public view returns (string memory) {
        user memory doc = userList[i];
	return doc.email;
    }

    function getUserType(uint i) public view returns (string memory) {
        user memory doc = userList[i];
	return doc.user_type;
    }

   function getAuctionName(uint i) public view returns (string memory) {
        auction memory doc = auctionList[i];
	return doc.auctioner_name;
    }

    function getAuctionId(uint i) public view returns (string memory) {
        auction memory doc = auctionList[i];
	return doc.auction_id;
    }

    function getAuctionDetails(uint i) public view returns (string memory) {
        auction memory doc = auctionList[i];
	return doc.auction_details;
    }
    
    function getMinimumAmount(uint i) public view returns (string memory) {
        auction memory doc = auctionList[i];
	return doc.minimum_amount;
    }

    function getStartDate(uint i) public view returns (string memory) {
        auction memory doc = auctionList[i];
	return doc.start_date;
    }

    function getEnddate(uint i) public view returns (string memory) {
        auction memory doc = auctionList[i];
	return doc.end_date;
    }

    function getCategory(uint i) public view returns (string memory) {
        auction memory doc = auctionList[i];
	return doc.auction_category;
    }

    function getBidAuctionId(uint i) public view returns (string memory) {
        bid memory doc = bidList[i];
	return doc.auction_id;
    }

    function getBidder(uint i) public view returns (string memory) {
        bid memory doc = bidList[i];
	return doc.bidder;
    }

    function getAmount(uint i) public view returns (string memory) {
        bid memory doc = bidList[i];
	return doc.amount;
    }

    function getBidDate(uint i) public view returns (string memory) {
        bid memory doc = bidList[i];
	return doc.bid_date;
    }
    function getTransactionType(uint i) public view returns (string memory) {
        bid memory doc = bidList[i];
	return doc.transaction_type;
    }
    
}