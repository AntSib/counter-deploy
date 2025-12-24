import { useEffect, useState } from "react";
import {
  getCounter,
  increment,
  decrement,
  reset,
} from "./api/counter";

export default function App() {
  const [value, setValue] = useState<number>(0);

  const load = async () => {
    const res = await getCounter();
    setValue(res.data.value);
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <div style={{ textAlign: "center", marginTop: "4rem" }}>
      <h1>Counter</h1>
      <h2>{value}</h2>
      <div style={{ display: "flex", gap: "1rem", justifyContent: "center" }}>
        <button onClick={async () => setValue((await decrement()).data.value)}>
          -
        </button>
        <button onClick={async () => setValue((await increment()).data.value)}>
          +
        </button>
        <button onClick={async () => setValue((await reset()).data.value)}>
          Сброс
        </button>
      </div>
    </div>
  );
}
