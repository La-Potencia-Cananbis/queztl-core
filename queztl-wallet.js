/**
 * 🦅 QUEZTL WALLET CONNECTOR
 * Connect MetaMask, WalletConnect, Coinbase Wallet
 */

class QueztlWallet {
  constructor(config) {
    this.config = config;
    this.provider = null;
    this.account = null;
    this.chainId = null;
  }

  // Connect MetaMask
  async connectMetaMask() {
    if (typeof window.ethereum === 'undefined') {
      throw new Error('MetaMask no está instalado buey! Instálalo: https://metamask.io');
    }

    try {
      const accounts = await window.ethereum.request({ 
        method: 'eth_requestAccounts' 
      });
      
      this.provider = window.ethereum;
      this.account = accounts[0];
      this.chainId = await this.getChainId();

      console.log('🦅 Wallet conectada:', this.account);
      console.log('⛓️ Chain ID:', this.chainId);

      // Listen for account changes
      this.provider.on('accountsChanged', (accounts) => {
        this.account = accounts[0];
        console.log('🔄 Account changed:', this.account);
      });

      // Listen for chain changes
      this.provider.on('chainChanged', (chainId) => {
        this.chainId = chainId;
        console.log('🔄 Chain changed:', chainId);
        window.location.reload();
      });

      return {
        account: this.account,
        chainId: this.chainId,
        provider: this.provider
      };
    } catch (error) {
      console.error('❌ Error conectando wallet:', error);
      throw error;
    }
  }

  // Switch Network
  async switchNetwork(networkName) {
    const network = this.config.networks[networkName];
    if (!network) throw new Error(`Network ${networkName} no encontrada`);

    try {
      await this.provider.request({
        method: 'wallet_switchEthereumChain',
        params: [{ chainId: network.chainId }]
      });
    } catch (error) {
      // If network not added, add it
      if (error.code === 4902) {
        await this.provider.request({
          method: 'wallet_addEthereumChain',
          params: [{
            chainId: network.chainId,
            chainName: network.name,
            rpcUrls: [network.rpc],
            blockExplorerUrls: [network.explorer],
            nativeCurrency: network.currency
          }]
        });
      } else {
        throw error;
      }
    }
  }

  // Get Chain ID
  async getChainId() {
    return await this.provider.request({ method: 'eth_chainId' });
  }

  // Get Balance
  async getBalance(address = null) {
    const account = address || this.account;
    const balance = await this.provider.request({
      method: 'eth_getBalance',
      params: [account, 'latest']
    });
    return parseInt(balance, 16) / 1e18; // Convert to ETH
  }

  // Sign Message
  async signMessage(message) {
    const signature = await this.provider.request({
      method: 'personal_sign',
      params: [message, this.account]
    });
    return signature;
  }

  // Send Transaction
  async sendTransaction(to, value, data = '0x') {
    const txParams = {
      from: this.account,
      to: to,
      value: '0x' + (value * 1e18).toString(16),
      data: data
    };

    const txHash = await this.provider.request({
      method: 'eth_sendTransaction',
      params: [txParams]
    });

    console.log('📤 Transaction sent:', txHash);
    return txHash;
  }

  // Disconnect
  disconnect() {
    this.provider = null;
    this.account = null;
    this.chainId = null;
    console.log('👋 Wallet desconectada');
  }
}

// Export for browser
if (typeof window !== 'undefined') {
  window.QueztlWallet = QueztlWallet;
}

export default QueztlWallet;
