import React from "react";
import { ExternalLink } from "./legislator_utilities";

const Footer = () => {
  return (
    <footer className="bg-blue-900 text-white p-6">
      <div className="container mx-auto flex flex-row gap-10">
        <p className="text-sm">&copy; 2023 <ExternalLink text="Fred Buchanan" href="https://buchanan.one" gray={300}/>. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;
