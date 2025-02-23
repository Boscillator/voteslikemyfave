import { Html, Head, Main, NextScript } from "next/document";
import { Header } from "@/components/header";

export default function Document() {
  return (
    <Html lang="en">
      <Head />
      <body className="antialiased bg-gray-100">
        <Header />
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
