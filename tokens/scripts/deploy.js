async function main() {
  const [deployer] = await ethers.getSigners();

  console.log("Deploying contracts with the account:", deployer.address);

  const erc20 = await ethers.deployContract("MyERC20");
  const erc721 = await ethers.deployContract("MyERC721");
  const erc1155 = await ethers.deployContract("MyERC1155");

  console.log("ERC20 token address:", await erc20.getAddress());
  console.log("ERC721 token address:", await erc721.getAddress());
  console.log("ERC1155 token address:", await erc1155.getAddress());
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
