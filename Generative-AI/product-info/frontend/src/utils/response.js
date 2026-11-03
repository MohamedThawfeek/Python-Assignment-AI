function parseJson(value) {
  if (typeof value !== "string") return value;

  const cleanedValue = value
    .trim()
    .replace(/^```(?:json)?\s*/i, "")
    .replace(/\s*```$/, "");

  try {
    return JSON.parse(cleanedValue);
  } catch {
    return value;
  }
}

function extractCustomerResponse(value) {
  if (typeof value !== "string") return "";

  const cleanedValue = value
    .trim()
    .replace(/^```(?:text|markdown)?\s*/i, "")
    .replace(/\s*```$/, "");
  const customerResponse = cleanedValue.match(
    /response\s+to\s+(?:the\s+)?user\s*:\s*#{0,4}\s*([\s\S]*)$/i,
  );

  return (customerResponse?.[1] || cleanedValue)
    .trim()
    .replace(/^#{1,6}[ \t]*(?:\r?\n)+/, "")
    .trim();
}

export function normalizeResponse(payload) {
  const parsedPayload = parseJson(payload);
  const responseBody =
    parsedPayload && typeof parsedPayload === "object" ? parsedPayload : {};
  const parsedData = parseJson(responseBody.data);

  let products = [];
  let textResponse = "";

  if (Array.isArray(parsedData)) {
    products = parsedData;
  } else if (typeof parsedData === "string") {
    textResponse = extractCustomerResponse(parsedData);
  } else if (parsedData && typeof parsedData === "object") {
    const nestedProducts =
      parsedData.items || parsedData.products || parsedData.results || parsedData.data;
    products = Array.isArray(nestedProducts) ? nestedProducts : [parsedData];
  }

  return {
    message: textResponse || responseBody.message || "I received the response.",
    status: responseBody.status,
    products,
  };
}
