import {useState, useEffect} from 'react';
import { listCollectionItems } from '../services/api';

export const useListCollectionItems = (refreshTrigger) => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [collectionItems, setCollectionItems] = useState(null);

    const fetchCollectionItems = async () => {
        setLoading(true);
        setError(null);

        try {
            const items = await listCollectionItems();
            setCollectionItems(items);
        } catch (err) {
            const errorMessage = err.response?.data?.detail || err.message || 'Failed to fetch collection items';
            setError(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchCollectionItems();
    }, [refreshTrigger]);

    return {
        collectionItems,
        loading,
        error,
        refetch: fetchCollectionItems, // Expose refetch function
    };
};
