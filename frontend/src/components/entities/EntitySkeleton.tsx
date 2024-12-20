import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';


export function EntitySkeleton() {
    return (
        <Card>
            <CardHeader className="pb-2" >
                <Skeleton className="h-6 w-1/3" />
                <Skeleton className="h-4 w-1/4" />
            </CardHeader>
            < CardContent >
                <Skeleton className="h-4 w-2/3" />
            </CardContent>
        </Card>
    );
}

export function EntityListSkeleton() {
    return (

        <div className="space-y-4" >
            <Skeleton className="h-10 w-full" />
            <div className="grid gap-4" >
                {
                    [...Array(3)].map((_, i) => (
                        <EntitySkeleton key={i} />
                    ))
                }
            </div>
        </div>
    );
}