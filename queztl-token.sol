// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * 🦅 QUEZTL TOKEN - $QZTL
 * The fastest AI training and rendering token in the universe
 */

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract QueztlToken is ERC20, Ownable {
    // Token Details
    uint256 public constant MAX_SUPPLY = 1_000_000_000 * 10**18; // 1 billion tokens
    uint256 public constant INITIAL_SUPPLY = 100_000_000 * 10**18; // 100M initial

    // Staking rewards
    mapping(address => uint256) public stakedAmount;
    mapping(address => uint256) public stakingTimestamp;
    uint256 public constant STAKING_REWARD_RATE = 10; // 10% APY

    // AI Training rewards
    mapping(address => uint256) public trainingContributions;
    mapping(address => uint256) public renderingContributions;

    event Staked(address indexed user, uint256 amount);
    event Unstaked(address indexed user, uint256 amount, uint256 reward);
    event TrainingReward(address indexed user, uint256 amount);
    event RenderingReward(address indexed user, uint256 amount);

    constructor() ERC20("Queztl Token", "QZTL") Ownable(msg.sender) {
        _mint(msg.sender, INITIAL_SUPPLY);
    }

    // Stake tokens
    function stake(uint256 amount) external {
        require(amount > 0, "Cannot stake 0");
        require(balanceOf(msg.sender) >= amount, "Insufficient balance");

        // Claim existing rewards if any
        if (stakedAmount[msg.sender] > 0) {
            claimStakingRewards();
        }

        _transfer(msg.sender, address(this), amount);
        stakedAmount[msg.sender] += amount;
        stakingTimestamp[msg.sender] = block.timestamp;

        emit Staked(msg.sender, amount);
    }

    // Unstake tokens
    function unstake(uint256 amount) external {
        require(stakedAmount[msg.sender] >= amount, "Insufficient staked amount");

        uint256 reward = calculateStakingReward(msg.sender);
        
        stakedAmount[msg.sender] -= amount;
        _transfer(address(this), msg.sender, amount);
        
        if (reward > 0) {
            _mint(msg.sender, reward);
        }

        emit Unstaked(msg.sender, amount, reward);
    }

    // Calculate staking rewards
    function calculateStakingReward(address user) public view returns (uint256) {
        if (stakedAmount[user] == 0) return 0;

        uint256 stakingDuration = block.timestamp - stakingTimestamp[user];
        uint256 reward = (stakedAmount[user] * STAKING_REWARD_RATE * stakingDuration) / (365 days * 100);
        
        return reward;
    }

    // Claim staking rewards
    function claimStakingRewards() public {
        uint256 reward = calculateStakingReward(msg.sender);
        require(reward > 0, "No rewards to claim");

        stakingTimestamp[msg.sender] = block.timestamp;
        _mint(msg.sender, reward);
    }

    // Reward for AI training contribution
    function rewardTraining(address user, uint256 epochs) external onlyOwner {
        uint256 reward = epochs * 10 * 10**18; // 10 QZTL per epoch
        trainingContributions[user] += epochs;
        _mint(user, reward);

        emit TrainingReward(user, reward);
    }

    // Reward for rendering contribution
    function rewardRendering(address user, uint256 frames) external onlyOwner {
        uint256 reward = frames * 1 * 10**18; // 1 QZTL per frame
        renderingContributions[user] += frames;
        _mint(user, reward);

        emit RenderingReward(user, reward);
    }

    // Burn tokens
    function burn(uint256 amount) external {
        _burn(msg.sender, amount);
    }

    // Get user stats
    function getUserStats(address user) external view returns (
        uint256 balance,
        uint256 staked,
        uint256 pendingRewards,
        uint256 trainingContribs,
        uint256 renderingContribs
    ) {
        return (
            balanceOf(user),
            stakedAmount[user],
            calculateStakingReward(user),
            trainingContributions[user],
            renderingContributions[user]
        );
    }
}
