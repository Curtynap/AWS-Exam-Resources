exports.handler = async (event) => {
    // The event will be the transformed request from API Gateway VTL
    // Example: { "searchName": "Curtis", "searchCategory": "books", "requestId": "abc-123" }
    
    console.log("Received transformed event:", JSON.stringify(event, null, 2));

    const name = event.searchName || "Guest";
    const category = event.searchCategory || "general items";

    const items = [
        { id: 1, name: `${name}'s Guide to ${category}` },
        { id: 2, name: `Top 10 ${category} for ${name}` }
    ];

    // We return raw data here, NOT a proxy response object like { statusCode: 200, body: ... }
    // API Gateway will receive this raw object and transform it using the response mapping template.
    return {
        items: items,
        receivedRequestId: event.requestId
    };
};
