import { Html, Head, Main, NextScript } from "next/document";
import {Header} from "@/components/header";

export default function Document() {
  return (
    <Html lang="en">
      <Head />
      <body className="antialiased">
        <div className="bg-gray-100 h-screen">
          <Header />
          <Main />
          <NextScript />
        </div>
      </body>
    </Html>
  );
}
