import { useRouter } from "next/router";

export default function Legislator() {
  const router = useRouter();
  return <p>{router.query.lastname}</p>
}
