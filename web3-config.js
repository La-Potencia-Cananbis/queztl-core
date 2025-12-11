/**
 * 🦅 QUEZTL WEB 3.0 CONFIGURATION
 * Blockchain integration for the most powerful AI system
 */

export const WEB3_CONFIG = {
  // Supported Networks
  networks: {
    ethereum: {
      chainId: '0x1',
      name: 'Ethereum Mainnet',
      rpc: 'https://eth.llamarpc.com',
      explorer: 'https://etherscan.io',
      currency: { name: 'ETH', symbol: 'ETH', decimals: 18 }
    },
    polygon: {
      chainId: '0x89',
      name: 'Polygon Mainnet',
      rpc: 'https://polygon-rpc.com',
      explorer: 'https://polygonscan.com',
      currency: { name: 'MATIC', symbol: 'MATIC', decimals: 18 }
    },
    base: {
      chainId: '0x2105',
      name: 'Base Mainnet',
      rpc: 'https://mainnet.base.org',
      explorer: 'https://basescan.org',
      currency: { name: 'ETH', symbol: 'ETH', decimals: 18 }
    }
  },

  // Smart Contract Addresses (deploy your own)
  contracts: {
    queztlToken: '0x0000000000000000000000000000000000000000', // Deploy QUEZTL token
    aiMarketplace: '0x0000000000000000000000000000000000000000', // NFT marketplace
    renderingPool: '0x0000000000000000000000000000000000000000', // Decentralized rendering
    trainingDAO: '0x0000000000000000000000000000000000000000'  // DAO governance
  },

  // IPFS Configuration
  ipfs: {
    gateway: 'https://ipfs.io/ipfs/',
    pinataApi: 'https://api.pinata.cloud',
    web3Storage: 'https://api.web3.storage'
  },

  // Wallet Settings
  walletConnect: {
    projectId: 'YOUR_WALLETCONNECT_PROJECT_ID', // Get from cloud.walletconnect.com
    chains: [1, 137, 8453], // Ethereum, Polygon, Base
    methods: ['eth_sendTransaction', 'personal_sign'],
    events: ['chainChanged', 'accountsChanged']
  }
};

export default WEB3_CONFIG;
